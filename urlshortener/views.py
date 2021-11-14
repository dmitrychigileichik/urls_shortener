from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from .forms import ShortenerForm, RegisterUserForm, LoginUserForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Shortener


@login_required
def home_view(request):
    template = 'urlshortener/home.html'
    context = dict()
    context['form'] = ShortenerForm()
    context['title'] = 'Shortener'
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
            try:
                shortened_object = Shortener.objects.get(long_url=used_form.cleaned_data['long_url'], user=request.user)
            except (KeyError, Shortener.DoesNotExist):
                shortened_object = used_form.save(commit=False)
                shortened_object.user = request.user
                shortened_object.save()
            new_url = request.build_absolute_uri('/redirect/') + shortened_object.short_url
            long_url = shortened_object.long_url
            context['new_url'] = new_url
            context['long_url'] = long_url
            context['user'] = request.user.username
            return render(request, template, context)
        context['errors'] = used_form.errors
        return render(request, template, context)


def intro(request):
    template = 'urlshortener/intro.html'
    context = dict()
    context['title'] = 'Intro page'
    return render(request, template, context)


def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
    except (KeyError, Shortener.DoesNotExist):
        raise Http404('Sorry this link is broken')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'urlshortener/register.html'
    success_url = reverse_lazy('shortener:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'urlshortener/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log in'
        return context


def logout_user(request):
    logout(request)
    return redirect('shortener:login')


class UserShorts(LoginRequiredMixin, ListView):
    model = Shortener
    template_name = 'urlshortener/index.html'
    context_object_name = 'urls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My urls'
        return context

    def get_queryset(self):
        return Shortener.objects.filter(user=self.request.user)

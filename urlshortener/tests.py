from django.test import TestCase, Client
from .forms import ShortenerForm


class RedirectTest(TestCase):
    def setUP(self):
        self.client = Client()

    def test_main_page_status(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/',  status_code=302, target_status_code=200)

    def test_urls_page_status(self):
        response = self.client.get('/urls/')
        self.assertRedirects(response, '/login/?next=/urls/',  status_code=302, target_status_code=200)


class FormsTest(TestCase):
    def test_url_form(self):
        form_data = {'long_url': 'something'}
        form = ShortenerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {'long_url': ['Enter a valid URL.']})

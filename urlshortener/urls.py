from django.urls import path

# Import the home view
from .views import *


app_name = "shortener"
urlpatterns = [
    path('', intro, name='intro'),
    path('home/', home_view, name='home'),
    path('redirect/<str:shortened_part>', redirect_url_view, name='redirect'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('urls/', UserShorts.as_view(), name='urls'),

]

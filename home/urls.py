from django.urls import path
from .views import HomeTest

app_name = 'home'
urlpatterns = [
    path('', HomeTest.as_view(), name='home'),
]
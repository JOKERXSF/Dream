from django.urls import path,re_path
from Dreamapp import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('registry/',views.registry,name='registry')
]

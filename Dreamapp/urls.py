from django.urls import path,re_path,include
from Dreamapp import views,utils,ut

urlpatterns = [
    path('login/',views.login,name='login'),
    path('registry/',views.registryView.as_view()),
    path('checkuname/',ut.checkuname),
    path('password_reset/<int:user_pk>/<str:token>/',views.reset_password_confirm,name='reset_password_confirm'),
    #path('password_reset/',views.reset_password_confirm,name='reset_password_confirm'),
    path('home/',views.home,name='home'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('logOut/',views.logOut,name="logOut"),
    path('selfInfo/', views.selfInfo, name='selfInfo'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('company/', views.company, name="company"),
    path('companyTags/', views.companyTags, name="companyTags"),
]

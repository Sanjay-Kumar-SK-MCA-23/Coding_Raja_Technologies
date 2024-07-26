from django.urls import path
from .import views

urlpatterns=[
    path('index',views.index,name='indexpage'),
    path('register',views.register,name='register'),
    path('login',views.login,name='loginpage'),
    path('logout',views.logout,name='logoutpage'),
    path('sentimentdata',views.sentimentdata,name='sentimentpage'),
    path('sentiment',views.sentiment,name='sentimentalvalue')
]
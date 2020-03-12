from django.urls import path

from . import views


app_name = 'signUp'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('reg/', views.reg, name = 'reg'),
	path('log/', views.log, name = 'log'),
	path('logout/', views.logout, name = 'logout'),
	path('password_change/', views.password_change, name = 'password_change'),
]
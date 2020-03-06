from django.urls import path

from . import views


app_name = 'signUp'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:user_id>/', views.detail, name = 'detail'),
	path('reg/', views.reg, name = 'reg'),
]
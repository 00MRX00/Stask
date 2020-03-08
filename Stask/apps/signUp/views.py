from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

import hashlib

from .models import User, UserLogPass
from .forms import SignUpForm

def index(request):
	latest_users_list = User.objects.order_by('-user_reg_date')[:5]
	signUpForm = SignUpForm()
	return render(request, 'signUp/list.html', {'latest_users_list': latest_users_list, 'signUpForm': signUpForm})

def detail(request, user_id):
	try:
		user = User.objects.get(id = user_id)
		userLogPass = UserLogPass.objects.get(user_id = user.id)
	except:
		raise Http404("Пользователь не найден!")

	return render(request, 'signUp/detail.html', {'user': user, 'userLogPass': userLogPass})

def reg(request):
	if(request.method == "POST"):
		signUpForm = SignUpForm(request.POST)
		if(signUpForm.is_valid()):
			user = {
				"name": signUpForm.cleaned_data["user_name"],
				"surname": signUpForm.cleaned_data["user_surname"],
				"patronymic": signUpForm.cleaned_data["user_patronymic"],
				"email": signUpForm.cleaned_data["user_email"],
				"birthdate": signUpForm.cleaned_data["user_birthdate"],
				"reg_date": timezone.now(),
				"password": signUpForm.cleaned_data["user_password"],
				"conf_password": signUpForm.cleaned_data["user_conf_password"]
			}
			if(user["password"] == user["conf_password"]):
				us = User(user_name=user["name"], user_surname=user["surname"], user_patronymic=user["patronymic"], user_birthdate=user["birthdate"], user_reg_date=user["reg_date"])
				us.save()
				usLP = UserLogPass(user = us, user_email=user["email"], user_password=hashlib.sha512(str(user["password"]).encode()).hexdigest())
				usLP.save()
			else:
				raise Http404("Пароли не совпадают!")
	
	return HttpResponseRedirect(reverse('signUp:index'))
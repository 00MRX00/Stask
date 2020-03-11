from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core import serializers

import hashlib, re

from .models import User, UserLogPass
from .forms import SignUpForm, SignInForm

def index(request):
	latest_users_list = User.objects.order_by('-user_reg_date')
	# latest_users_list = User.objects.all()
	return render(request, 'signUp/index.html', {'latest_users_list': latest_users_list})

def detail(request, user_id):
	try:
		user = User.objects.get(id = user_id)
		userLogPass = UserLogPass.objects.get(user_id = user.id)
	except:
		raise Http404("Пользователь не найден!")

	return render(request, 'signUp/detail.html', {'user': user, 'userLogPass': userLogPass})

def reg(request):
	if request.method == "POST":
		signUpForm = SignUpForm(request.POST)
		hasError = False
		if signUpForm.is_valid():
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
			if re.compile('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-_]).{8,}$').search(user["password"]):
				if(user["password"] == user["conf_password"]):
					allUsers = UserLogPass.objects.filter(user_email=user["email"])
					if(not allUsers):
						try:
							us = User(user_name=user["name"], user_surname=user["surname"], user_patronymic=user["patronymic"], user_birthdate=user["birthdate"], user_reg_date=user["reg_date"])
							us.save()
							hashPass = hashlib.sha512(str(user["password"]).encode()).hexdigest()
							usLP = UserLogPass(user = us, user_email=user["email"], user_password = hashPass)
							usLP.save()
							messages.add_message(request, messages.SUCCESS, 'Пользователь успешно зарегистрирован')
						except:
							messages.add_message(request, messages.ERROR, 'Ошибка регистрации пользователя!')
					else:
						messages.add_message(request, messages.ERROR, 'Пользователь с данным "Email" уже существует!')
				else:
					messages.add_message(request, messages.ERROR, 'Пароли не совпадают!')
			else:
				messages.add_message(request, messages.ERROR, 'Пароль слишком простой! В пароле должно быть хотя бы 8 символов, 1 заглавная английская буква, 1 строчная английская буква, 1 цифра и 1 спец. символ (#,?,!,@,$, ,%,^,&,*,-,_)')
		else:
			signUpFormFields = {
				"user_name": "Имя",
				"user_surname": "Фамилия",
				"user_patronymic": "Отчество",
				"user_email": "Email",
				"user_birthdate": "Дата рождения",
				"user_password": "Пароль",
				"user_conf_password": "Подтвердите пароль",
			}
		for error in signUpForm.errors:
			messages.add_message(request, messages.ERROR, 'Поле "' + signUpFormFields[str(error)] + '" заполнено неверно!')
		for mes in messages.get_messages(request):
			if mes.tags == "error":
				hasError = True
				break
		messages.get_messages(request).used = False
		if hasError:
			return HttpResponseRedirect(reverse('signUp:reg'))
		else:
			return HttpResponseRedirect(reverse('signUp:index'))
	else:
		signUpForm = SignUpForm()
		return render(request, 'signUp/signup.html', {'signUpForm': signUpForm})
	

def log(request):
	if request.method == "POST":
		signInForm = SignInForm(request.POST)
		hasError = False
		if signInForm.is_valid():
			form = {
					"email": signInForm.cleaned_data["user_email"],
					"password": signInForm.cleaned_data["user_password"]
				}
		searchUser = UserLogPass.objects.filter(user_email=form["email"])
		if searchUser:
			hashPass = hashlib.sha512(str(form["password"]).encode()).hexdigest()
			if hashPass == searchUser[0].user_password:
				currentUser = User.objects.get(pk=searchUser[0].user_id)
				request.session["currentUser"] = currentUser.jsonEncoder()
				messages.add_message(request, messages.SUCCESS, 'Авторизация прошла успешно')
			else:
				messages.add_message(request, messages.ERROR, 'Неверный пароль')
		else:
			messages.add_message(request, messages.ERROR, 'Пользователь с таким "Email" не зарегистрирован')
		for mes in messages.get_messages(request):
			if mes.tags == "error":
				hasError = True
				break
		messages.get_messages(request).used = False
		if hasError:
			return HttpResponseRedirect(reverse('signUp:log'))
		else:
			return HttpResponseRedirect(reverse('signUp:index'))
	else:
		signInForm = SignInForm()
		return render(request, 'signUp/signin.html', {'signInForm': signInForm})
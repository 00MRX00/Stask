from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

import hashlib, re

from .models import User, UserLogPass
from .forms import SignUpForm

def index(request):
	latest_users_list = User.objects.order_by('-user_reg_date')[:5]
	return render(request, 'signUp/index.html', {'latest_users_list': latest_users_list})

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
		hasError = False
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
			if(re.compile('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-_]).{8,}$').search(user["password"])):
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
			if not hasError:
				hasError = True
			messages.add_message(request, messages.ERROR, 'Поле "' + signUpFormFields[str(error)] + '" заполнено неверно!')
		if hasError:
			return HttpResponseRedirect(reverse('signUp:reg'))
		else:
			return HttpResponseRedirect(reverse('signUp:index'))
	else:
		signUpForm = SignUpForm()
		return render(request, 'signUp/signup.html', {'signUpForm': signUpForm})
	

def authorize(request):
	pass
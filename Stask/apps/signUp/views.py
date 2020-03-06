from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User
from .forms import SignUpForm

def index(request):
	latest_users_list = User.objects.order_by('-user_reg_date')[:5]
	signUpForm = SignUpForm()
	return render(request, 'signUp/list.html', {'latest_users_list': latest_users_list, 'signUpForm': signUpForm})

def detail(request, user_id):
	try:
		a = User.objects.get(id = user_id)
	except:
		raise Http404("Пользователь не найден!")

	return render(request, 'signUp/detail.html', {'signUp': a})

def reg(request):
	#error = ""
	if(request.method == "POST"):
		signUpForm = SignUpForm(request.POST)
		if(signUpForm.is_valid()):
			user = {
				"name": signUpForm.cleaned_data["user_name"],
				"surname": signUpForm.cleaned_data["user_surname"],
				"patronymic": signUpForm.cleaned_data["user_patronymic"],
				"email": signUpForm.cleaned_data["user_email"],
				"birthdate": signUpForm.cleaned_data["user_birthdate"],
				"reg_date": timezone.now()
			}
			try:
				us = User(user_name=user["name"], user_surname=user["surname"], user_patronymic=user["patronymic"], user_email=user["email"], user_birthdate=user["birthdate"], user_reg_date=user["reg_date"])
				us.save()
				#error = "Пользователь успешно зарегистрирован."
			except:
				raise Http404("Пользователь не зарегистрирован!")
				#error = "Не удалось зарегистрировать пользователя!"
		#else:
			#error = "Некорректно введены данные!"
	
	return HttpResponseRedirect(reverse('signUp:index'))
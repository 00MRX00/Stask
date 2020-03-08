import datetime
from django.db import models

from django.utils import timezone

class User(models.Model):
	user_name = models.CharField('Имя пользователя', max_length = 50)
	user_surname = models.CharField('Фамилия пользователя', max_length = 50)
	user_patronymic = models.CharField('Отчество пользователя', max_length = 50)
	user_birthdate = models.DateTimeField('Дата рождения')
	user_reg_date = models.DateTimeField('Дата регистрации')
	user_type = models.CharField('Тип пользователя', max_length = 50, default = "user")

	def __str__(self):
		string = self.user_surname + " " + str(self.user_name)[0] + "." + str(self.user_patronymic)[0] + "." 
		return string

	def was_registered_recently(self):
		return self.user_reg_date >= (timezone.now() - datetime.timedelta(days = 1))

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	
# q = User(user_name="Александр", user_surname="Олейников", user_patronymic="Павлович", user_email="17515560@mail.ru", user_birthdate=datetime(2000,5,31,0,0,0,0,tzinfo=pytz.UTC), user_reg_date=timezone.now())

class UserLogPass(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	user_email = models.EmailField('Email пользователя', max_length = 50)
	user_password = models.CharField('Пароль пользователя', max_length = 200)

	def __str__(self):
		string = str(self.user) 
		return string

	class Meta:
		verbose_name = 'Логин/Пароль'
		verbose_name_plural = 'Логины/Пароли'


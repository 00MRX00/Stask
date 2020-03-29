import datetime, json
from django.db import models

from django.utils import timezone

class User(models.Model):
	id = models.AutoField(primary_key=True)
	user_name = models.CharField('Имя пользователя', max_length = 50)
	user_surname = models.CharField('Фамилия пользователя', max_length = 50)
	user_patronymic = models.CharField('Отчество пользователя', max_length = 50)
	user_birthdate = models.DateTimeField('Дата рождения')
	user_reg_date = models.DateTimeField('Дата регистрации')
	user_type = models.CharField('Тип пользователя', max_length = 50, default = "user")

	def __str__(self):
		if self.user_patronymic:
			string = self.user_surname + " " + str(self.user_name)[0] + "." +  str(self.user_patronymic)[0] + "." 
		else:
			string = self.user_surname + " " + str(self.user_name)[0] + "." 
		return string

	def was_registered_recently(self):
		return self.user_reg_date >= (timezone.now() - datetime.timedelta(days = 1))

	def jsonEncoder(self):
		us = {
			"user_id": str(self.id),
			"user_name" : str(self.user_name),
			"user_surname" : str(self.user_surname),
			"user_patronymic" : str(self.user_patronymic),
			"user_birthdate" : str(self.user_birthdate),
			"user_reg_date" : str(self.user_reg_date),
			"user_type" : str(self.user_type)
		}
		return json.dumps(us)

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	
# q = User(user_name="Тест", user_surname="Тестов", user_patronymic="Тестович", user_email="test@test.ru", user_birthdate=datetime(2010,10,10,0,0,0,0,tzinfo=pytz.UTC), user_reg_date=timezone.now())

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


class Project(models.Model):
	id = models.AutoField(primary_key=True)
	project_title = models.CharField('Название проекта', max_length = 255)
	project_description = models.TextField('Описание проекта', max_length = 3000)
	project_creation_date =  models.DateTimeField('Дата создания проекта')

	def __str__(self):
		return self.project_title

	class Meta:
		verbose_name = 'Проект'
		verbose_name_plural = 'Проекты'

class ProjectUsers(models.Model):
	id = models.AutoField(primary_key=True)
	project = models.ForeignKey(Project, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	user_type = models.CharField('Тип пользователя', max_length = 50, default = "undistributed")

	def __str__(self):
		string = str(self.project) + " - " + str(self.user)
		return string

	class Meta:
		verbose_name = 'Участник проекта'
		verbose_name_plural = 'Участники проектов'


class Task(models.Model):
	id = models.AutoField(primary_key=True)
	project = models.ForeignKey(Project, on_delete = models.CASCADE)
	task_title = models.CharField('Заголовок задания', max_length = 255)
	task_description = models.TextField('Описание задания', max_length = 3000)
	task_creation_date = models.DateTimeField('Дата создания задания')
	start_date = models.DateTimeField('Начало выполнения задания')
	end_date = models.DateTimeField('Конец выполнения задания')
	is_public = models.BooleanField('Публичное задание', default=False)
	done = models.BooleanField('Задание выполнено', default=False)

	def __str__(self):
		return str(self.project) + " - " + self.task_title

	class Meta:
		verbose_name = 'Задание'
		verbose_name_plural = 'Задания'


class TaskUsers(models.Model):
	id = models.AutoField(primary_key=True)
	task = models.ForeignKey(Task, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		string = str(self.task) + " - " + str(self.user)
		return string

	class Meta:
		verbose_name = 'Ответственный за задание'
		verbose_name_plural = 'Ответственные за задания'

class Todo(models.Model):
	id = models.AutoField(primary_key=True)
	task = models.ForeignKey(Task, on_delete = models.CASCADE)
	text = models.TextField('Текст TODO', max_length = 3000)
	done = models.BooleanField('TODO выполнено', default=False)

	def __str__(self):
		if len(str(self.text)) > 30:
			string = str(self.task) + " - " + str(self.text)[:30]
		else:
			string = str(self.task) + " - " + str(self.text)
		return string
from django import forms
 
class SignUpForm(forms.Form):
    user_name = forms.CharField(label = "Имя:", required = True, max_length = 50)
    user_surname = forms.CharField(label = "Фамилия:", required = True, max_length = 50)
    user_patronymic = forms.CharField(label = "Отчество:", required = False, max_length = 50)
    user_email = forms.EmailField(label = "Email:", required = True, min_length = 5, max_length = 50)
    user_birthdate = forms.DateField(label = "Дата рождения:", required = True)
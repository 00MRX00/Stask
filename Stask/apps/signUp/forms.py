from django import forms
 
class SignUpForm(forms.Form):
    user_name = forms.CharField(label = "Имя:", required = True, max_length = 50)
    user_surname = forms.CharField(label = "Фамилия:", required = True, max_length = 50)
    user_patronymic = forms.CharField(label = "Отчество:", required = False, max_length = 50)
    user_email = forms.EmailField(label = "Email:", required = True, min_length = 5, max_length = 50)
    user_birthdate = forms.DateField(label = "Дата рождения:", required = True)
    user_password = forms.CharField(widget=forms.PasswordInput(), label = "Пароль:", required = True)
    user_conf_password = forms.CharField(widget=forms.PasswordInput(), label = "Подтвердите пароль:", required = True)

class SignInForm(forms.Form):
    user_email = forms.EmailField(label = "Email:")
    user_password = forms.CharField(widget=forms.PasswordInput(), label = "Пароль:")
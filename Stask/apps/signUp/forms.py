from django import forms
 
class SignUpForm(forms.Form):
    user_name = forms.CharField(label = "Имя:", required = True, max_length = 50)
    user_surname = forms.CharField(label = "Фамилия:", required = True, max_length = 50)
    user_patronymic = forms.CharField(label = "Отчество:", required = False, max_length = 50)
    user_email = forms.EmailField(label = "Email:", required = True, max_length = 50)
    user_birthdate = forms.DateField(label = "Дата рождения:", required = True)
    user_password = forms.CharField(widget=forms.PasswordInput(), label = "Пароль:", required = True)
    user_conf_password = forms.CharField(widget=forms.PasswordInput(), label = "Подтвердите пароль:", required = True)

class SignInForm(forms.Form):
    user_email = forms.CharField(label = "Email:", max_length = 50)
    user_password = forms.CharField(widget=forms.PasswordInput(), label = "Пароль:")

class PassChangeForm(forms.Form):
    user_cur_password = forms.CharField(widget=forms.PasswordInput(), label = "Старый пароль:")
    user_new_password = forms.CharField(widget=forms.PasswordInput(), label = "Новый пароль:")
    user_new_password2 = forms.CharField(widget=forms.PasswordInput(), label = "Подтвердите пароль:")
        
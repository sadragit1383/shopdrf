from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# customer user form in admin panel
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(label='رمز عبور',widget=forms.PasswordInput,max_length=100)
    re_password = forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput,max_length=100)

    class Meta:
        model = CustomUser
        fields = ['mobile_number','name','family','email','gender']



    def clean_re_password(self):
        re_password = self.cleaned_data['re_password']
        password = self.cleaned_data['password']

        if re_password and password and password != re_password:
            raise ValidationError('تکرار رمز نادرست میباشد')


        return re_password


# change password in admin page
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text = 'برای تغییر رمز عبور رو  <a href="../password">لینک</a> بزنید')

    class Meta:
        model = CustomUser
        fields = '__all__'
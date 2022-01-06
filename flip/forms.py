from django.contrib.auth import forms
from django import forms
from django.core.exceptions import ValidationError
from flip.models import *
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm, AuthenticationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Username','class':'_INMUI'}
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Full Name','class':'_INMUI'}
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder':'Email Address','class':'_INMUI'}
    ))
    phone = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder':'Phone','class':'_INMUI'}
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':'Password','class':'_INMUI'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':'Confirm Password','class':'_INMUI'}
    ))
    class Meta:
        model = UserAccounts
        fields = ['username','email','first_name','phone']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = UserAccounts.objects.get(email=email)
        except Exception as e:
            return email
        raise ValidationError(f'{email} is already exists.')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = UserAccounts.objects.get(username=username)
        except Exception as e:
            return username
        raise ValidationError(f'{username} is already exists.')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop('autofocus',None)



class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Email Address','class':'_INMUI'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':'Password','class':'_INMUI'}
    ))

    def __init__(self, *args, **kwargs):
        super(AuthenticationUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus',None)



class PostUploadForm(forms.ModelForm):
    class Meta:
        model = PostUploadModel
        fields = ['post','caption','post_type']
        widgets = {
            'post':forms.FileInput(attrs={'class':'form-control mt-4'}),
            'caption':forms.Textarea(attrs={'class':'form-control mt-4 _CDFF', 'id':'dis_id', 'placeholder':'Post discription...'}),
            'post_type':forms.Select(attrs={'class':'form-select mt-4'}),
        }


class UsersEditsForm(UserChangeForm):
    password = None
    class Meta:
        model = UserAccounts
        fields = ['image','username','first_name','email','phone']
        widgets = {
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CommentsModels
        fields = ['body']
        widgets = {
            'body':forms.Textarea(
                attrs={'class':'_COMGH me-auto', 'id':'com_id', 'placeholder':' Add comment here...'}
            )
        }


class ChangePasswordCLassForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Old Password'}
    ))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'New Password'}
    ))
    new_password2 = forms.CharField(label='New Confirm Password',widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'New Confirm Password'}
    ))


class BasicInfoForm(forms.ModelForm):
    web_link = forms.CharField(label='URL Link',widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'URL Link'}
    ))
    bio = forms.CharField(label='Bio',widget=forms.Textarea(
        attrs={'class':'form-control _CDFF','placeholder':'Bio'}
    ))
    class Meta:
        model = BasicInfoModel
        fields = ['web_link','bio']


class ForgetPasswordForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder':'Enter your register email','class':'_INMUI'}
    ))


class PasswordResetSetForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':'New Password','class':'_INMUI'}
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':'New Confirm Password','class':'_INMUI'}
    ))
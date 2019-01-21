""" The forms for the team_fundraiser app
"""
from django import forms
from datetime import datetime
from .models import Fundraiser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DonationForm(forms.Form):
    """ Form for a new Donation, which can be tied to a specific fundraiser """

    name = forms.CharField()
    amount = forms.CharField()
    other_amount = forms.CharField(required=False)
    email = forms.EmailField()
    anonymous = forms.BooleanField(required=False)
    date = datetime.now()

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'required': False, 'rows': 3}
        )
    )

    def clean(self):
        # Use the amount or "other amount" from the form

        try:
            amount = self.cleaned_data['amount']
        except KeyError:
            amount = ""

        try:
            other_amount = self.cleaned_data['other_amount']
        except KeyError:
            other_amount = ""

        if amount == 'other' or amount == '':
            # TODO pull out just the number, in case they added a $
            try:
                amount = float(other_amount)
            except ValueError:
                raise forms.ValidationError("Amount is not a number")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.is_staff = False
        user.is_admin = False

        if commit:
            user.save()

        return user


class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ('campaign', 'name', 'goal', 'message')

    def __init__(self, *args, **kwargs):
        super(FundraiserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

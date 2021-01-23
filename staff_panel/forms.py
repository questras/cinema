from django.forms import ModelForm, Form
from django.forms import DateTimeField, DateTimeInput
from django.forms import EmailField
from cinema.models import Showing


class CreateShowingForm(ModelForm):
    when = DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Showing
        fields = ('when', 'movie', 'hall')


class SelectUserForm(Form):
    email = EmailField(label="User's e-mail address")

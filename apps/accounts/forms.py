import datetime
import string

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

#custom imports
from .models import Subject
from .models import Teacher


class UserAuthenticationForm(AuthenticationForm):
    """
    Extends the standard django AuthenticationForm, to support 75 character
    usernames.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:            
            if field in self.errors:
                self.fields[field].widget.attrs['class']='form-control'


class SubjectCreationForm(forms.ModelForm):
    """
    To Create Subjects
    """
    class Meta:
        model = Subject
        fields = ('name','code',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:            
            if field in self.errors:
                self.fields[field].widget.attrs['class']='form-control warning'
            else:
                self.fields[field].widget.attrs['class']='form-control'


class TeacherCreationForm(forms.ModelForm):
    """
    To Add Teachers
    """
    class Meta:
        model = Teacher
        fields = ('first_name','last_name',
                  'profile_pic','email',
                  'phone_number','subjects','room_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'] = forms.ModelMultipleChoiceField(Subject.objects.filter(is_active=True))
        for field in self.fields:            
            if field in self.errors:
                self.fields[field].widget.attrs['class']='form-control warning'
            else:
                self.fields[field].widget.attrs['class']='form-control'

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if email:
    #         validate_email(email)
    #         if Teacher.objects.filter(email=email).exists():
    #             raise forms.ValidationError("Email already exists")
    #         return self.cleaned_data

    def clean(self):
        related_objs = self.cleaned_data.get('subjects')
        if related_objs and related_objs.count() > 6:
            raise forms.ValidationError('Maximum 5 subjects are allowed.')        
        #email validation
        email = self.cleaned_data['email']
        if email:
            validate_email(email)
            if Teacher.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
        return self.cleaned_data
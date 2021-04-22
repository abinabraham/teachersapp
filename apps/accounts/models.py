# Author: Abin Abraham 
# -*- coding: utf-8 -*-
# Accounts related models will adde here

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

class User(AbstractUser):
    """
    add custom User fields here
    example: profile pic, dob, address

    I'm just make this with pass statment
    for the updation later on Profile Fields

    must include UserManager() as object
    """
    pass

class Subject(models.Model):
    '''
    Master model of Subject
    Fields - Code and name
    eg: EN-english, AR-arabic
    '''
    name = models.CharField(
        _('Name'), max_length=255, blank=True)
    code = models.CharField(_('Code'), 
         max_length=255, unique=True)
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('This subject should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_created = models.DateTimeField(_('date created'),
                                       default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)                            
    

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Teacher(models.Model):
    '''

    Teachers can have the same first name and last name \
    but their email address should be unique.
    A teacher can teach no more than 5 subjects.
    '''
    first_name = models.CharField(
        _('First name'), max_length=255, blank=True)
    last_name = models.CharField(
        _('Last name'), max_length=255, blank=True)
    profile_pic = models.ImageField(_('Profile picture'), upload_to='profile',
                default='img/avatar5.png')
    email = models.EmailField(_('Email address'), 
         unique=True)
    phone_number = models.CharField(
        _('Phone Number (with country code)'), max_length=255, blank=True) 
    room_number = models.CharField(
        _('Room Number'), max_length=255, blank=True)   
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('This user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    subjects = models.ManyToManyField(
        'Subject', verbose_name=_("Subjects"), blank=True)

    date_joined = models.DateTimeField(_('date joined'),
                                       default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)    

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

'''
Author: Abin
In this file Dashaboard related Views and functions \
Added
'''

import json
import csv
import pandas as pd
import os.path

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from pathlib import Path

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

#Custom URLs
from apps.accounts import forms as account_forms
from apps.accounts.models import (Teacher,
                                     Subject)

# ================
# Dashboard Views
# ================

class IndexView(generic.TemplateView):
    """
    An overview view which displays Teachers list.

    Supports the permission-based dashboard. 
    Only Superuser can view the dashboard, 
    As it is Superadmin dashboard
    """
    subject_form_class = account_forms.SubjectCreationForm
    teacher_form_class = account_forms.TeacherCreationForm
    page_title = "Teachers"


    def get_template_names(self):
        if self.request.user.is_staff:
            return ['dashboard/home.html', ]
        else:
            return ['dashboard/index_nonstaff.html']

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['subject_form'] = self.subject_form_class
        ctx['teacher_form'] = self.teacher_form_class 
        ctx['subject_list'] = self.active_subject_list()
        ctx['page_title'] = self.page_title 
        subject_filter = self.request.GET.get('subject_filter')
        filter_lname = self.request.GET.get('filter_lname')
        ctx['subject_filter'] = subject_filter
        ctx['filter_lname'] = filter_lname        
        ctx['teachers_list'] = self.active_teacher_list(subject_filter,
                                                filter_lname)
        return ctx

    def post(self, request, *args, **kwargs):
        if 'subject_submit' in request.POST:
            return self.validate_subject_form(request)
        if 'teacher_submit' in request.POST:
            return self.validate_teacher_form(request)
        return http.HttpResponseBadRequest()
    
    def validate_subject_form(self, request):
        subject_form = self.subject_form_class(request.POST)
        if subject_form.is_valid():
            self.sub_object = subject_form.save()            
            msg = self.get_subject_success_message(subject_form)
            if msg:
                messages.success(self.request, msg)
            return redirect(self.get_success_url(subject_form))
        else:
            msg = self.get_error_message(subject_form)            
            messages.error(self.request, ",".join(msg))         

        ctx = self.get_context_data(subject_form=subject_form)
        return self.render_to_response(ctx)
    
    def validate_teacher_form(self, request):
        teacher_form = self.teacher_form_class(request.POST, request.FILES)
        if teacher_form.is_valid():
            self.teacher_object = teacher_form.save() 
            msg = self.get_teacher_success_message(teacher_form)
            if msg:
                messages.success(self.request, msg)
        else:
            msg = self.get_error_message(teacher_form)            
            messages.error(self.request, ",".join(msg))     

        ctx = self.get_context_data(teacher_form=teacher_form)
        return self.render_to_response(ctx)


    def get_subject_success_message(self, form):
        return _("Subject created successfully")

    def get_teacher_success_message(self, form):
        return _("Teacher created successfully")

    def get_error_message(self, form):
        msgs = []
        for error in form.errors.values():
            msgs.append(error.as_text())
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        return clean_msgs

    def get_success_url(self, form):
        return settings.INDEX_URL

    def active_teacher_list(self, sub=None, fltr=None):
        queryset = Teacher.objects.filter(is_active=True)
        if sub:
            queryset = queryset.filter(subjects__code = sub)
        if fltr and fltr != "All":
            queryset = queryset.filter(last_name__istartswith = fltr)
        return queryset

    def active_subject_list(self):
        _subjects = Subject.objects.filter(is_active=True)
        return _subjects



class SubjectsView(generic.TemplateView):
    """
    Class will render active subjects to template
    if non staff authenticated will redirect to non_staff page

    """
    template_name = "dashboard/subjects.html"
    page_title = "Subjects"

    def get_template_names(self):
        if self.request.user.is_staff:
            return ['dashboard/subjects.html', ]
        else:
            return ['dashboard/index_nonstaff.html']
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['subject_list'] = self.active_subject_list()
        ctx['page_title'] = self.page_title 
        return ctx

    def active_subject_list(self):
        _subjects = Subject.objects.filter(is_active=True)
        return _subjects


class ProfileDetailView(DetailView):
    """
    Profile detail view
    """

    model = Teacher
    template_name = "accounts/profile.html"
    page_title = "Profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):
        if self.request.user.is_staff:
            return ['accounts/profile.html', ]
        else:
            return ['dashboard/index_nonstaff.html']


class ImporterView(generic.TemplateView):
    """
    An overview file importer
    """
    page_title = "Importer"


    def get_template_names(self):
        if self.request.user.is_staff:
            return ['dashboard/importer.html', ]
        else:
            return ['dashboard/index_nonstaff.html']

    def post(self, request, *args, **kwargs):
        return self.validate_form()

    # need to update this function later with some generic function
    def validate_form(self):
        path = self.request.FILES.get('file')
        sub_data = {}
        try:
            df=pd.read_csv(path,sep=',')
            teachers = []
            for i in range(len(df)):
                email_row = df.iloc[i][3]
                if email_row and type(email_row) == str:
                    try:
                        f = open(os.path.join(PROJECT_PATH+'/teachers/public/media/teachers/', df.iloc[i][2]))
                    except Exception as e:
                        df.iloc[i][2] = "avatar5.png"
                    subjects = df.iloc[i][6].split(",")
                    for subject in subjects:
                        q_set = Subject.objects.filter(name=subject)
                        if not q_set:
                            Subject.objects.create(name=subject, code=subject)
                    sub_data[df.iloc[i][3]] = subjects
                    if not Teacher.objects.filter(email=email_row).exists():                    
                        teachers.append(
                            Teacher(
                            first_name=df.iloc[i][0],
                            last_name=df.iloc[i][1],
                            email=df.iloc[i][3],
                            profile_pic=df.iloc[i][2],
                            phone_number=df.iloc[i][4],
                            room_number=df.iloc[i][5]     
                            )
                        )
                    
                else:
                    pass
            try:
                teachers_obj = Teacher.objects.bulk_create(teachers)
                msg = "Successfully imported data."  
                messages.success(self.request, msg)                
            except Exception as e:
                msg = "Oops something happened."         
                messages.error(self.request, msg)
        except Exception as e:
            msg = "Oops something happened. Please check the file format"         
            messages.error(self.request, msg)    
        ctx = self.get_context_data()
        update_teacher_with_subjects(**sub_data)
        return self.render_to_response(ctx)

def active_teacher_list():
    queryset = Teacher.objects.filter(is_active=True)
    return queryset

def get_subject(code):
    _subject = Subject.objects.filter(code=code)[0]
    return _subject
    
def update_teacher_with_subjects(**kwargs):
    teacher_list =  active_teacher_list()
    try:
        for teacher in teacher_list:
            for sub in kwargs[teacher.email]:
                subject = get_subject(sub)
                teacher.subjects.add(subject)
    except Exception as e:
        print("Logging: something error happened while updating subjects", e)
    return True
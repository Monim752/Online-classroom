from django.views.generic.base import View
from oursystem.models import  Course, Subject, Comment
from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, CreateView,
                                    UpdateView, DeleteView, DetailView, ListView, FormView)
from django.urls import reverse_lazy, reverse
from .forms import CourseForm, CommentForm, ReplyForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.


class SubjectListView(ListView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'oursystem/subject_list_view.html'

class CourseListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'oursystem/course_list_view.html'


"""class JoinClass(DetailView, FormView):
    form_class = CourseForm
    fields = ('code')
    context_object_name = 'subjects'
    model = Subject
    template_name = 'oursystem/join_class.html'


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('oursystem:course_list',kwargs={'slug':self.object.slug})"""


class CourseDetailView(DetailView, FormView):
    context_object_name = 'courses'
    model = Course
    template_name = 'oursystem/course_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        subject = self.object.subject
        return reverse_lazy('oursystem:course_detail',kwargs={'subject':subject.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.course_name = self.object.comments.name
        fm.course_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class CourseCreateView(CreateView):
    #fields = ('course_id','name','section','code')
    form_class = CourseForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'oursystem/course_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('oursystem:course_list',kwargs={'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class CourseUpdateView(UpdateView):
    fields = ('name','section','ppt','pdf')
    model= Course
    template_name = 'oursystem/course_update.html'
    context_object_name = 'courses'

class CourseDeleteView(DeleteView):
    model= Course
    context_object_name = 'courses'
    template_name = 'oursystem/course_delete.html'

    def get_success_url(self):
        print(self.object)
        subject = self.object.subject
        return reverse_lazy('oursystem:course_list',kwargs={'slug':subject.slug})
from django.views.generic.base import View
from oursystem.models import Course, Comment
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, CreateView,
                                    UpdateView, DeleteView, DetailView, ListView, FormView)
from django.urls import reverse_lazy, reverse
from .forms import CourseForm, CommentForm, ReplyForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

class CourseListView(ListView):
    context_object_name = 'courses'
    model = Course
    template_name = 'oursystem/course_list_view.html'

# def course_view(request):
#     context = {}
#
#     # add the dictionary during initialization
#     context["dataset"] = Course.objects.all()
#
#     return render(request, "oursystem/course_list_view.html", context)

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

# def course_detail(request, course_id):
#     models = Course
#     form_class = CommentForm
#     second_form_class = ReplyForm
#     course = get_context_data(models, pk=course_id)
#     context = {'course': course}
#     return render(request, 'course_detail.html', context)

class CourseDetailView(DetailView, FormView, ListView):
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
        course = self.object.course
        return reverse_lazy('oursystem:course_detail',kwargs={'pk': self.pk})
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

# def course_create(request):
#     # dictionary for initial data with
#     # field names as keys
#     context = {}
#
#     # add the dictionary during initialization
#     form = CourseForm(request.POST or None)
#     if form.is_valid():
#         fm = form.save(commit=False)
#         fm.created_by = request.user
#         fm.save()
#
#     context['form'] = form
#     return render(request, "oursystem/course_create.html", context)


class CourseCreateView(CreateView):
    #fields = ('course_id','name','section','code')
    # import pdb;
    # pdb.set_trace()
    form_class = CourseForm
    context_object_name = 'course'
    model = Course
    template_name = 'oursystem/course_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('oursystem:course_list')

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class CourseUpdateView(UpdateView):
    fields = ('name', 'description', 'duration', 'start_date', 'end_date')
    model = Course
    template_name = 'oursystem/course_update.html'
    context_object_name = 'courses'


class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'courses'
    template_name = 'oursystem/course_delete.html'

    def get_success_url(self):
        self.object = self.get_object()
        print(self.object)
        subject = self.object.subject
        return reverse_lazy('oursystem:course_list', kwargs={'pk': self.pk})
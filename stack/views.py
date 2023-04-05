from django.shortcuts import render,redirect

# Create your views here.
from stack.forms import LoginForm,RegistrationForm,QuestionForm
from django.contrib.auth.models import User
from django.views.generic import View,CreateView,FormView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout

from stack.models import Answers, Questions
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"u must be login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decorators=[signin_required,never_cache]

class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self, request,*args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("successfull")
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})
@method_decorator(decorators,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=QuestionForm
    model=Questions
    success_url=reverse_lazy("home")
    context_object_name="questions"
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

# localhost:8000/questions/1/answers/add
decorators
def add_answer(request,*args, **kwargs):
    question_id=kwargs.get("id")
    ques=Questions.objects.get(id=question_id)
    ans=request.POST.get("answer")
    ques.answers_set.create(answer=ans,user=request.user)
    return redirect("home")
decorators
def upvote_view(request,*args, **kwargs):
    ans_id=kwargs.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.up_vote.add(request.user)
    ans.save()
    return redirect("home")
decorators
def sign_out(request,*args, **kwargs):
    logout(request)
    return redirect("signin")

class MyQuestionView(ListView):
    model=Questions
    context_object_name="questions"
    template_name="myquestions.html"

    def get_queryset(self):
        return Questions.objects.filter(user=self.request.user)
    


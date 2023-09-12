from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import UserLogin, UserSignUp 
from django.http import HttpResponseRedirect
from django.views.generic import  View
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.


class HomeView(LoginRequiredMixin,View):
    template_name = "UserAuth/home.html"
    context = {}
    def get(self, request):
        return render(request, self.template_name, self.context)

def login_user(request):
    form = UserLogin()
    next = ""
    if request.GET:  
        next = request.GET['next']
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            if next == "":
                return redirect('home')
            else:
                return HttpResponseRedirect(next)

    context = {
        'form': form,
        'next': next
    }
    return render(request, 'UserAuth/login.html', context)

def register_user(request):
    form = UserSignUp()
    if request.method == "POST":
        form = UserSignUp(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'UserAuth/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


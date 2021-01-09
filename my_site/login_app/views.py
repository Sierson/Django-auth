from django.shortcuts import render
from .forms import UserForm, UserInfoForm
from .models import UserInfo

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def home(request):
    context = {}
    if request.user.is_authenticated:
        curr_user = request.user
        user_id = curr_user.id
        basic_info = User.objects.get(pk=user_id)
        more_info = UserInfo.objects.get(user__pk=user_id)

        context.update({'basic_info': basic_info})
        context.update({'more_info': more_info})
    
    return render(request, 'login_app/index.html', context=context)

def login_me(request):
    return render(request, 'login_app/login.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Account is not active")
        else:
            return HttpResponse("Wrong Login or Password")
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def logout_me(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        user_info_form = UserInfoForm(data = request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']

            user_info.save()

            registered = True

    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()
        
    context = {'UserForm': user_form, 'UserInfoForm': user_info_form, 'registered': registered}
    return render(request, 'login_app/register.html', context=context)
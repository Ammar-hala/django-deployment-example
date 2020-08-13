from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import authenticate , login , logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#from basic_app.models import User,UserProfileInfo
from basic_app.forms import UserForm,UserProfileInfoForm
# from . import forms then will have to acces like forms.UserForm
# Create your views here.
def index(request):
    return render(request , 'basic_app/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in, NICE ")


@login_required #should be one line above func
def user_logout(request): #called decorator which ensure this view will be accessed only if user is logged in
    logout(request) #automatically logsout user.. builtin
    return HttpResponseRedirect( reverse('index') )



def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # goes in settings.py and saves pass as ahash
            user.save() # grabbing user form saving it in data base... hashingn pass.. and then save that pass to database

            profile = profile_form.save(commit=False) #not commiting to databse yet cos neet to alter some data
            profile.user = user # defining that OneToOne relationship here
            #chek if they provide a profile pic
            if 'profile_pic' in request.FILES: #use this technique when user uploads some file and deal with it by the key we used for it
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors , profile_form.errors )


    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request , 'basic_app/registration.html' ,
                  {'user_form':user_form ,
                  'profile_form':profile_form ,
                  'registered':registered} )



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username') #get('username') because in login html we used name='username' in input of username
        password = request.POST.get('password')

        #django's builtin authentication funcs
        user = authenticate(username=username , password=password)

        if user:
            if user.is_active:
                login(request , user) #
                return HttpResponseRedirect( reverse('index') )
                #if  user logs in and they're succesful and account is active it will redirect user to homepage

            else:
                return HttpResponse('Account Not Active')

        else: # will be printed just for us
            print("Somone Tried To Login and Failed")
            print("User name : {} and password {}".format(user_login , password) )
            return HttpResponse('Invalid login details supplied')

    else: # request.method was'mt POST mtlb habent submitted anything
        return render(request , 'basic_app/login.html')

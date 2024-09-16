from django.shortcuts import render, redirect
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from django.db.models import Q


# Create your views here.
class Main(View):
    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect("home")
        
        return render(request, template_name='app/main.html')
    
    
    
class Login(View):
    def get(self, request):
        return render(request, template_name='app/login.html')
    
    def post(self,request):
        data = request.POST.dict()
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate(request=request,username=username, password=password)
        if user!=None:
            login(request, user)
            return redirect("home")
        
        context = {"error":"there is something wrong"}
        
        return render(request, template_name='app/login.html',context=context)

class Register(View):
    def get(self, request):
        return render(request, template_name='app/register.html')
    
    def post(self, request):
        context = {}
        data = request.POST.dict()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        try:
            new_user = User()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            
            new_user.save()
              
            user = authenticate(request=request, username=username, password=password)
            if user != None:
                login(request=request,user=user)
                return redirect("home")
        except:
            context.update({"error":"the data is wrong"})

            
        return render(request, template_name='app/register.html',context=context)
        

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("main")
        
    

class Home(View):
    def get(self, request):
        
        
        if request.user.is_authenticated:
            users = User.objects.all()
            context = {'user':request.user,'users':users}
            return render(request, template_name='app/home.html',context=context)
        return redirect("main")

class Chat_person(View):
    def get(self, request, id):
        person = User.objects.get(id=id)
        me = request.user
        
        messages = models.Message.objects.filter(Q(from_who = me, to_who = person) |Q( to_who = me, from_who = person)).order_by("date","time")
        
        context ={"person":person, "me":me, "messages":messages}
        return render(request, template_name='app/chat_person.html', context=context)
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate,logout

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from user_management.forms import LoginUserForm, UserRegisterForm



class UserRegisterView(View):
    def post(self,request,*args,**kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect("admin:login")
        
        for field, errors in form.errors.items():
            field_name = form.fields[field].label if form.fields[field].label else field
            for error in errors:
                messages.error(request, f"{field_name}: {error}!!")
        return render(request, "register.html", context={"form":form})


    def get(self,request,*args,**kwargs):
        form = UserRegisterForm()
        context = {
            "form":form
        }
        return render(request,"register.html",context=context) 



class LoginUserView(View):
    def get(self,request,*args,**kwargs):
        form = LoginUserForm()
        return render(request,"login.html",context={"form":form})

    def post(self,request,*args,**kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email =  form.data.get("email")
            password = form.data.get("password")
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                return redirect("report:home_page")
            
        for field, errors in form.errors.items():
            field_name = form.fields[field].label if form.fields[field].label else field
            for error in errors:
                messages.error(request, f"{field_name}: {error}!!")
        # return render(request, "register.html", context={"form":UserRegisterForm()})
        return render(request,"login.html",context={"form":form})
    

class LogOutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("report:home_page")
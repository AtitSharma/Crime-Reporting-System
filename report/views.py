from django.shortcuts import render,redirect,get_object_or_404
from django.views import View

from report.forms import ContactDetailForm, ReportCreationForm, ReportUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

from report.models import CrimeReport
from django.contrib import messages

# Create your views here.


class HomePageView(View):

    def get_queryset(self):
        return CrimeReport.objects.filter(is_private=False)


    def get(self,request,*args,**kwargs):
        query = self.get_queryset()
        context = {
            "crime_reports": query,
        }
        return render(request,"home.html",context=context)




class ReportCrimeView(View):
    form_class = ReportCreationForm

    def get(self,request,*args,**kwargs):
        form = self.form_class()
        return render(request,"report.html",context={"form":form})
    

    def handle_error(self,form):
        for field, errors in form.errors.items():
            field_name = form.fields[field].label if form.fields[field].label else field
            for error in errors:
                messages.error(self.request, f"{field_name}: {error}!!")

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Crime Reported Successfully you will be notified soon .")
            return redirect("report:home_page")
        self.handle_error(form)
        return render(request,"report.html",context={"form":form})
    


class ReportCrimeDetailView(LoginRequiredMixin,View):

    def get_queryset(self):
        return get_object_or_404(CrimeReport,id=self.kwargs.get("id"))
    

    def get(self,request,*args,**kwargs):
        report = self.get_queryset()
        report.delete()
        return redirect("report:home_page")
    


class ReportCrimeUpdateView(LoginRequiredMixin,View):
    form_class = ReportUpdateForm

    def get_queryset(self):
        return get_object_or_404(CrimeReport,id=self.kwargs.get("id"))
    

    def get(self,request,*args,**kwargs):
        report = self.get_queryset()
        form = self.form_class(instance=report)
        return render(request,"report_update.html",context={"form":form})


    def handle_error(self,form):
        for field, errors in form.errors.items():
            field_name = form.fields[field].label if form.fields[field].label else field
            for error in errors:
                messages.error(self.request, f"{field_name}: {error}!!")


    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES,instance=self.get_queryset())
        if form.is_valid():
            form.save()
            messages.success(request,"Crime Reported Updated Successfully .")
            return redirect("report:home_page")
        self.handle_error(form)
        form =self.form_class()
        return render(request,"report_update.html",context={"form":form})
    


class ContactDetailsView(View):
    
    def get(self,request,*args,**kwargs):
        form = ContactDetailForm()
        return render(request,"phone_number.html",context={"form":form})
    
    def post(self,request,*args,**kwargs):
        return redirect("report:my-report",email=self.request.POST.get("email"),phone_number=self.request.POST.get("phone_number"))




class MyReportsView(View):
    def get_queryset(self):
        return CrimeReport.objects.filter(email=self.kwargs.get("email"),phone_number = self.kwargs.get("phone_number"))
    

    def get(self,request,*args,**kwargs):
        context = {"crime_reports":self.get_queryset()}
        return render(request,"myreports.html",context=context)
    

    
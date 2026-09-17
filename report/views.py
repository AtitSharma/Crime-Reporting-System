from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.db.models.functions import TruncDate, ExtractHour, ExtractWeekDay

from report.forms import ContactDetailForm, ReportCreationForm, ReportUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

from report.models import CrimeReport, PoliceStation
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


def get_filtered_queryset(request):
    qs = CrimeReport.objects.all()
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    station = request.GET.get('station')
    status = request.GET.get('status')
    if date_from:
        qs = qs.filter(crime_datetime__date__gte=date_from)
    if date_to:
        qs = qs.filter(crime_datetime__date__lte=date_to)
    if station:
        qs = qs.filter(report_taken_by_station__name=station)
    if status:
        qs = qs.filter(status=status)
    return qs


@staff_member_required
def analytics_api(request):
    all_stations = list(PoliceStation.objects.all().values_list('name', flat=True))
    qs = get_filtered_queryset(request)

    total = qs.count()
    pending = qs.filter(status='PENDING').count()
    investigating = qs.filter(status='INVESTIGATING').count()
    action_taken = qs.filter(status='ACTION_TAKEN').count()

    station_wise = list(
        qs.values('report_taken_by_station__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    station_data = [
        {"name": s['report_taken_by_station__name'] or 'Unassigned', "count": s['count']}
        for s in station_wise
    ]

    status_wise = list(
        qs.values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    time_wise = list(
        qs.filter(crime_datetime__isnull=False)
        .annotate(date=TruncDate('crime_datetime'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    time_data = [{"date": t['date'].strftime('%Y-%m-%d') if t['date'] else '', "count": t['count']} for t in time_wise]

    hourly_wise = list(
        qs.filter(crime_datetime__isnull=False)
        .annotate(hour=ExtractHour('crime_datetime'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('hour')
    )
    hourly_data = [{"hour": int(h['hour']), "count": h['count']} for h in hourly_wise]

    private_count = qs.filter(is_private=True).count()
    public_count = qs.filter(is_private=False).count()

    day_names = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
    weekday_wise = list(
        qs.filter(crime_datetime__isnull=False)
        .annotate(weekday=ExtractWeekDay('crime_datetime'))
        .values('weekday')
        .annotate(count=Count('id'))
        .order_by('weekday')
    )
    weekday_data = [{"day": day_names.get(int(w['weekday']), ''), "count": w['count']} for w in weekday_wise]

    recent = list(
        qs.order_by('-created_at')[:10]
        .values('id', 'title', 'status', 'created_at', 'name', 'report_taken_by_station__name')
    )
    for r in recent:
        r['created_at'] = r['created_at'].strftime('%Y-%m-%d %H:%M') if r['created_at'] else ''

    return JsonResponse({
        "total": total,
        "pending": pending,
        "investigating": investigating,
        "action_taken": action_taken,
        "all_stations": all_stations,
        "station_wise": station_data,
        "status_wise": list(status_wise),
        "time_wise": time_data,
        "hourly_wise": hourly_data,
        "private_count": private_count,
        "public_count": public_count,
        "weekday_wise": weekday_data,
        "recent_reports": recent,
    })
    
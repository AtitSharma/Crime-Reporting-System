from django.urls import path

from report.views import ContactDetailsView, HomePageView, MyReportsView, ReportCrimeView,ReportCrimeDetailView,ReportCrimeUpdateView

app_name = "report"



urlpatterns = [
    path("",HomePageView.as_view(),name="home_page"),
    path("reports/",ReportCrimeView.as_view(),name="report"),
    path("reports/delete/<int:id>/",ReportCrimeDetailView.as_view(),name="report-detail"),
    path("reports/update/<int:id>/",ReportCrimeUpdateView.as_view(),name="report-detail-update"),
    path("contact-details/",ContactDetailsView.as_view(),name="contact-details"),
    path("my-report/<str:phone_number>/<str:email>/",MyReportsView.as_view(),name="my-report")
]

from django.db import models

from user_management.models import TimeStampAbstractModel, User



class ActionStatus(models.TextChoices):
    PENDING = "PENDING"
    INVESTIGATING = "INVESTIGATING"
    ACTION_TAKEN = "ACTION_TAKEN"



class PoliceStation(TimeStampAbstractModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(blank=True,null=True,decimal_places=4,max_digits=10)
    longitude = models.DecimalField(blank=True,null=True,decimal_places=4,max_digits=10)



    def __str__(self):
        return self.name +" --->  " +self.location



class CrimeReport(TimeStampAbstractModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    proof_documents = models.FileField(upload_to="report/proof",blank=True,null=True)
    crime_datetime = models.DateTimeField(blank=True,null=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone_number = models.CharField(max_length=255)
    action_taken_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="action_taken_by_user",blank=True,null=True)
    status = models.CharField(choices=ActionStatus.choices,default=ActionStatus.PENDING)
    explanation = models.CharField(max_length=255,blank=True,null=True)
    report_taken_by_station = models.ForeignKey(PoliceStation,on_delete=models.SET_NULL,blank=True,null=True,related_name="report_taken_by_station")
    is_private = models.BooleanField(default=True)
    is_granted = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title + " ------>>>>     " + self.status.title()
from django.db import models
import uuid

# Create your models here.
class Manudetails(models.Model):
    contact = models.FloatField()
    prof = models.FileField(upload_to='profiles/dist/',default='/default.png',max_length=100, blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'manudetails'

class Products(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    pname = models.CharField(max_length=200, blank=True, null=True)
    mdate = models.CharField(max_length=50, blank=True, null=True)
    edate = models.CharField(max_length=50, blank=True, null=True)
    manufusrname = models.CharField(max_length=200)
    distusrname = models.CharField(max_length=200)
    verfied = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'products'
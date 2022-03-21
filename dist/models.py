from django.db import models

# Create your models here.
class QRUp(models.Model):
    qr_img= models.ImageField(upload_to='images/')

class ProfImg(models.Model):
    prof_img= models.ImageField(upload_to='profiles/')

class Distdetails(models.Model):
    contact = models.FloatField()
    prof = models.FileField(upload_to='profiles/dist/',default='/default.png',max_length=100, blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'distdetails'
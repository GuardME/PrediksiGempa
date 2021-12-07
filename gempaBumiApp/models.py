from django.db import models

# Create your models here.
class Gempa(models.Model):
    Lat = models.FloatField()
    Lon = models.FloatField()
    Depth = models.FloatField()
    Mag = models.FloatField()
    Region = models.CharField(max_length=250)
    Date = models.CharField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Gempa'

class Prediksi_Gempa(models.Model):
    Lat = models.FloatField()
    Lon = models.FloatField()
    Mag = models.FloatField()
    Depth = models.FloatField()
    Score = models.FloatField()
    
    class Meta:
        verbose_name_plural = 'Prediksi_Gempa'
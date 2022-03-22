from django.db import models

# Create your models here.
class morning(models.Model):
    num = models.IntegerField(primary_key=True)
    dujeong = models.CharField(max_length=50, null=True)
    cheon_station_am = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.num


class noon(models.Model):
    num = models.IntegerField(primary_key=True)
    fromschool = models.CharField(max_length=10, null=True)
    terminal = models.CharField(max_length=10, null=True)
    cheon_station_pm = models.CharField(max_length=10, null=True)

    #def __str__(self):
    #   return self.num

#######################################################################################################################




from django.db import models


# Create your models here.

class IotDevice(models.Model):
    id = models.AutoField(primary_key=True)
    device_id = models.CharField(max_length=200,
                                 unique=True
                                 )
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200)
    own_by_user = models.CharField(max_length=200, default='')

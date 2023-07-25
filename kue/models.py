from django.db import models
from uuid import uuid4


class KueIndonesia(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4)
	name = models.CharField(max_length=255, null=True)
	image = models.ImageField(upload_to='images/')
	prediction = models.CharField(max_length=50, null=True)
 
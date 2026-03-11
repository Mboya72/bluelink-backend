from django.db import models
from users.models import User

class Advertisement(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    image = models.ImageField(upload_to="ads/")

    start_date = models.DateField()

    end_date = models.DateField()

    approved = models.BooleanField(default=False)
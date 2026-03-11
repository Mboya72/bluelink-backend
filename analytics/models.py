from django.db import models
from users.models import User

class UserActivity(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    activity_type = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)


class ProductView(models.Model):

    product_id = models.IntegerField()

    viewer = models.ForeignKey(User, on_delete=models.CASCADE)

    viewed_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Profile is the proxy model that would be in a one-to-one relationship with the User. This will provide the other necessary details that the user might need.
DEFAULT_IMAGE = "user_images\default.png"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user_images', default = DEFAULT_IMAGE)
    middle_name = models.CharField(max_length=100)
    job_position = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)
    logged = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


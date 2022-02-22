from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_agent = models.BooleanField('agent stat', default=False)
    is_customer = models.BooleanField('customer status', default=False)
    REQUIRED_FIELDS = []


class Agent(models.Model):
    User = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


# Create your models here.
class Package(models.Model):
    title = models.CharField(max_length=100)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    cost = models.IntegerField()
    duration = models.IntegerField()
    Location = models.CharField(max_length=100)
    ddate = models.DateField()
    posteddate = models.DateField(auto_now=True)
    dloc = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slots = models.IntegerField(default=0)
    image = models.ImageField(null=True, default="1.jpg")

    class Meta:
        ordering = ['-posteddate']

    def __str__(self):
        return self.title


class book(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    time = models.DateField(auto_now=True)
    price = models.IntegerField()
    nos = models.IntegerField(default=1)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    

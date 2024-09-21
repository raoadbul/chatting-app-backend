from django.db import models

class Group(models.Model):
    name=models.CharField(max_length=50)
    timestamp=models.DateField(auto_now_add=True)


class Chat(models.Model):
    conversation=models.CharField(max_length=1500)
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    timestamp=models.DateField(auto_now=True)
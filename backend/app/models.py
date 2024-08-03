from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class User(models.Model):
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class App(models.Model):
    id = models.AutoField(primary_key=True)
    appName = models.CharField(max_length=100)
    lackDataNum = models.IntegerField()
    fuzzyDataNum = models.IntegerField()
    brokenLinkNum = models.IntegerField()

    lackData = models.TextField()
    fuzzyData = models.TextField()
    brokenLink = models.TextField()
    htmlUrl = models.TextField()

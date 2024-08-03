from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

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

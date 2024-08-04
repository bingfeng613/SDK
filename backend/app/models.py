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
    totalDataNum = models.IntegerField()
    totalUrlNum = models.IntegerField()

    lackDataNum = models.IntegerField()
    fuzzyDataNum = models.IntegerField()

    lackData = models.TextField()
    fuzzyData = models.TextField()

    UnableToConnectNum = models.IntegerField()
    NotPrivacyPolicyNum = models.IntegerField()
    appPrivacyPolicyNum = models.IntegerField()
    notDataInsidePrivacyPolicyNum = models.IntegerField()

    UnableToConnectLink = models.TextField()
    NotPrivacyPolicyLink = models.TextField()
    appPrivacyPolicyLink = models.TextField()
    notDataInsidePrivacyPolicyLink = models.TextField()

    brokenLinkNum = models.IntegerField()
    brokenLink = models.TextField()

    htmlUrl = models.TextField()

class MyCosConfig(models.Model):
    bucket_name = models.CharField(max_length=255, unique=True, verbose_name='存储桶名称')
    region = models.CharField(max_length=255, verbose_name='腾讯云区域')
    secret_id = models.CharField(max_length=255, verbose_name='腾讯云 SecretId')
    secret_key = models.CharField(max_length=255, verbose_name='腾讯云 SecretKey')
    def __str__(self):
        return self.bucket_name
    class Meta:
        verbose_name = '腾讯云 COS 配置'
        verbose_name_plural = '腾讯云 COS 配置'

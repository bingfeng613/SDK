# Generated by Django 5.0.7 on 2024-08-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="app",
            name="appName",
            field=models.CharField(default="app", max_length=100),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-02 13:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_app_htmlurl"),
    ]

    operations = [
        migrations.AlterField(
            model_name="app",
            name="htmlUrl",
            field=models.CharField(max_length=500),
        ),
    ]

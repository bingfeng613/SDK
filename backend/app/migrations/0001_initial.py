# Generated by Django 5.0.7 on 2024-08-02 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="App",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("lackDataNum", models.IntegerField()),
                ("fuzzyDataNum", models.IntegerField()),
                ("brokenLinkNum", models.IntegerField()),
                ("lackData", models.TextField()),
                ("fuzzyData", models.TextField()),
                ("brokenLink", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("account", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
    ]

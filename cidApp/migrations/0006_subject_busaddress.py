# Generated by Django 5.0.6 on 2024-09-18 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cidApp', '0005_subject_pob'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='busaddress',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-08 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_certificates_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='cv',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
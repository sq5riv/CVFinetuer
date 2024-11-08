# Generated by Django 5.1.1 on 2024-11-08 05:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_person_photo_offers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skills',
            old_name='knowledge_level',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='skillsexperience',
            old_name='certificate',
            new_name='experience',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='description',
        ),
        migrations.RemoveField(
            model_name='person',
            name='gender',
        ),
        migrations.AlterField(
            model_name='certificates',
            name='cert_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.ImageField(upload_to='backend/foto/'),
        ),
        migrations.CreateModel(
            name='ExperienceCertificates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.certificates')),
                ('experience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.experience')),
            ],
        ),
        migrations.CreateModel(
            name='ExperienceDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('experience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.experience')),
            ],
        ),
    ]

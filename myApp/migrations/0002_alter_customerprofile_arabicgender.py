# Generated by Django 5.0.6 on 2024-06-01 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='arabicGender',
            field=models.CharField(blank=True, choices=[('ذكر', 'ذكر'), ('انثي', 'انثى')], max_length=20, null=True),
        ),
    ]

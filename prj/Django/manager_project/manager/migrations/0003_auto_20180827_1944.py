# Generated by Django 2.0.7 on 2018-08-27 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_person_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0003_lamar_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lamar',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-10 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jobseeker", "0002_delete_answerkuesioners_delete_excel_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cv",
            name="users_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
# Generated by Django 5.1 on 2024-08-16 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consultations", "0005_alter_booking_unique_together_alter_booking_slot"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="url",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
    ]

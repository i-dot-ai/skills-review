# Generated by Django 3.2.16 on 2023-01-14 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skills", "0006_auto_20230114_1548"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recommendation",
            name="image_url",
            field=models.CharField(max_length=2048),
        ),
    ]

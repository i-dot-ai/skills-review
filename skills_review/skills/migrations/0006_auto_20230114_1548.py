# Generated by Django 3.2.16 on 2023-01-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0005_auto_20230114_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='image_url',
            field=models.CharField(default=None, max_length=256, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='job_title',
            field=models.CharField(max_length=256),
        ),
    ]

# Generated by Django 3.2.15 on 2022-09-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0003_auto_20220907_0806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skill',
            old_name='has_delete_action',
            new_name='has_delete_flag',
        ),
        migrations.RenameField(
            model_name='skill',
            old_name='has_rename_action',
            new_name='has_rename_flag',
        ),
        migrations.RemoveField(
            model_name='suggestion',
            name='action',
        ),
        migrations.AddField(
            model_name='suggestion',
            name='flag',
            field=models.CharField(blank=True, choices=[('Not a skill', 'Not a skill'), ('Wrong name', 'Wrong name'), ('Multiple skills', 'Multiple skills'), ('Wrong category', 'Wrong category'), ('None', 'None')], max_length=256, null=True),
        ),
    ]

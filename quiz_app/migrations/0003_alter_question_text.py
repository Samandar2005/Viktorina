# Generated by Django 5.1.2 on 2024-11-07 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0002_rename_participant_name_answer_user_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(),
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_teacher_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=10),
        ),
    ]

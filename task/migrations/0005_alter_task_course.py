# Generated by Django 3.2.8 on 2021-12-15 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_usercourse_course'),
        ('task', '0004_task_created_at_task_do_up_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.course', verbose_name='Course'),
        ),
    ]

# Generated by Django 3.2.10 on 2023-06-02 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_alter_course_users'),
        ('task', '0018_alter_task_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='course.course', verbose_name='Course'),
        ),
    ]

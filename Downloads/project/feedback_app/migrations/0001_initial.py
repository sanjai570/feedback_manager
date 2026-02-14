"""
Migration: 0001_initial

This migration creates the initial database structure for the Feedback Collection System
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('IT', 'Information Technology'), ('CS', 'Computer Science'), ('ECE', 'Electronics & Communication'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('EE', 'Electrical Engineering'), ('OTHER', 'Other')], max_length=50)),
                ('year', models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')], max_length=10)),
                ('subject_or_faculty', models.CharField(max_length=200)),
                ('rating', models.IntegerField()),
                ('feedback_message', models.TextField()),
                ('is_anonymous', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Feedback',
                'ordering': ['-created_at'],
            },
        ),
    ]

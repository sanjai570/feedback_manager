# Migration: 0002_event_based_feedback_system

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_app', '0001_initial'),
    ]

    operations = [
        # Create Event model
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('event_date', models.DateTimeField()),
                ('venue', models.CharField(max_length=200)),
                ('organizer', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='events/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-event_date'],
            },
        ),

        # Create StudentProfile model
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('IT', 'Information Technology'), ('CS', 'Computer Science'), ('ECE', 'Electronics & Communication'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('EE', 'Electrical Engineering'), ('OTHER', 'Other')], max_length=50)),
                ('year', models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),

        # Create EventAttendance model
        migrations.CreateModel(
            name='EventAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to='feedback_app.event')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_attendances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'event')},
            },
        ),

        # Rename old Feedback model - we'll replace it
        # First, remove old Feedback model
        migrations.RemoveField(
            model_name='feedback',
            name='id',
        ),

        # Delete old feedback table
        migrations.DeleteModel(
            name='Feedback',
        ),

        # Create new Feedback model
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('feedback_message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback_app.event')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Feedback',
                'ordering': ['-created_at'],
                'unique_together': {('student', 'event')},
            },
        ),

        # Add unique constraint for EventAttendance
        migrations.AlterUniqueTogether(
            name='eventattendance',
            unique_together={('student', 'event')},
        ),
    ]

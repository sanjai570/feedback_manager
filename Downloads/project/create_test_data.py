#!/usr/bin/env python
"""
Create test data for Supabase database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')
django.setup()

from django.contrib.auth.models import User
from feedback_app.models import StudentProfile, Event, EventAttendance, Feedback
from django.utils import timezone
from datetime import timedelta

def create_test_data():
    """Create comprehensive test data for the system"""
    
    print("=" * 60)
    print("CREATING TEST DATA FOR SUPABASE")
    print("=" * 60)
    
    # 1. Create Admin User
    print("\n1. Creating Admin User...")
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@college.edu',
            'first_name': 'System',
            'last_name': 'Admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"   ✅ Admin created: admin / admin123")
    else:
        print(f"   ℹ️  Admin already exists")
    
    # 2. Create Student Users
    print("\n2. Creating Student Users with Profiles...")
    students_data = [
        {
            'username': 'student1',
            'email': 'john.doe@college.edu',
            'first_name': 'John',
            'last_name': 'Doe',
            'profile': {'department': 'CS', 'year': '3'}
        },
        {
            'username': 'student2',
            'email': 'jane.smith@college.edu',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'profile': {'department': 'ECE', 'year': '2'}
        },
        {
            'username': 'student3',
            'email': 'mike.johnson@college.edu',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'profile': {'department': 'ME', 'year': '4'}
        },
        {
            'username': 'student4',
            'email': 'sara.williams@college.edu',
            'first_name': 'Sara',
            'last_name': 'Williams',
            'profile': {'department': 'CS', 'year': '1'}
        }
    ]
    
    students = []
    for student_data in students_data:
        profile_data = student_data.pop('profile')
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults=student_data
        )
        
        if created:
            user.set_password('password123')
            user.save()
            
        profile, p_created = StudentProfile.objects.get_or_create(
            user=user,
            defaults=profile_data
        )
        
        if created:
            print(f"   ✅ {student_data['first_name']} {student_data['last_name']} created ({student_data['username']} / password123)")
        else:
            print(f"   ℹ️  {student_data['first_name']} {student_data['last_name']} already exists")
        
        students.append(user)
    
    # 3. Create Sample Events
    print("\n3. Creating Sample Events...")
    now = timezone.now()
    events_data = [
        {
            'title': 'Python Workshop',
            'description': 'Learn Python fundamentals and advanced concepts',
            'event_date': now + timedelta(days=7),
            'venue': 'Computer Lab 1',
            'organizer': 'CSE Department'
        },
        {
            'title': 'Web Development Bootcamp',
            'description': 'Full-stack web development using Django and React',
            'event_date': now + timedelta(days=15),
            'venue': 'Main Hall',
            'organizer': 'Tech Club'
        },
        {
            'title': 'AI and Machine Learning Hackathon',
            'description': 'Build AI models and compete for prizes',
            'event_date': now + timedelta(days=30),
            'venue': 'Innovation Center',
            'organizer': 'AI Lab'
        },
        {
            'title': 'Database Design Seminar',
            'description': 'Understanding SQL and NoSQL databases',
            'event_date': now + timedelta(days=21),
            'venue': 'Seminar Hall',
            'organizer': 'Database Group'
        },
        {
            'title': 'Cloud Computing Workshop',
            'description': 'AWS, GCP, and Azure cloud services',
            'event_date': now + timedelta(days=28),
            'venue': 'Conference Room',
            'organizer': 'Cloud Initiative'
        }
    ]
    
    events = []
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            event_date__date=event_data['event_date'].date(),
            defaults=event_data
        )
        
        if created:
            print(f"   ✅ {event.title} ({event.event_date.strftime('%Y-%m-%d')})")
        else:
            print(f"   ℹ️  {event.title} already exists")
        
        events.append(event)
    
    # 4. Create Event Attendances
    print("\n4. Creating Event Attendances...")
    attendance_count = 0
    for event in events[:3]:  # First 3 events
        for student in students[:3]:  # 3 students for each event
            attendance, created = EventAttendance.objects.get_or_create(
                student=student,
                event=event
            )
            if created:
                attendance_count += 1
    
    print(f"   ✅ {attendance_count} attendance records created")
    
    # 5. Create Feedback Records
    print("\n5. Creating Feedback Records...")
    feedback_count = 0
    feedback_messages = [
        "Excellent workshop! Learned a lot of new concepts.",
        "Great event, well-organized and informative.",
        "Very engaging and interactive sessions.",
        "Good content, would like more hands-on practice.",
        "Amazing experience, highly recommended!"
    ]
    
    for event in events[:3]:
        for student in students[:2]:
            rating = 4 + (hash(f"{student.username}{event.id}") % 2)  # 4 or 5
            message = feedback_messages[hash(f"{student.username}{event.id}") % len(feedback_messages)]
            
            feedback, created = Feedback.objects.get_or_create(
                student=student,
                event=event,
                defaults={
                    'rating': rating,
                    'feedback_message': message
                }
            )
            if created:
                feedback_count += 1
    
    print(f"   ✅ {feedback_count} feedback records created")
    
    # 6. Display Summary Statistics
    print("\n" + "=" * 60)
    print("TEST DATA SUMMARY")
    print("=" * 60)
    
    print(f"\n📊 DATABASE STATISTICS:")
    print(f"   • Total Users: {User.objects.count()}")
    print(f"   • Admin Users: {User.objects.filter(is_superuser=True).count()}")
    print(f"   • Student Profiles: {StudentProfile.objects.count()}")
    print(f"   • Events: {Event.objects.count()}")
    print(f"   • Event Attendances: {EventAttendance.objects.count()}")
    print(f"   • Feedback Records: {Feedback.objects.count()}")
    
    print(f"\n👤 TEST ACCOUNTS:")
    print(f"   ✓ Admin: admin / admin123")
    print(f"   ✓ Student 1: student1 / password123 (John Doe - CS Year 3)")
    print(f"   ✓ Student 2: student2 / password123 (Jane Smith - ECE Year 2)")
    print(f"   ✓ Student 3: student3 / password123 (Mike Johnson - ME Year 4)")
    print(f"   ✓ Student 4: student4 / password123 (Sara Williams - CS Year 1)")
    
    print(f"\n📅 SAMPLE EVENTS:")
    for event in Event.objects.all():
        feedback_count = Feedback.objects.filter(event=event).count()
        avg_rating = event.get_average_rating()
        print(f"   • {event.title}")
        print(f"     Date: {event.event_date.strftime('%B %d, %Y at %H:%M')}")
        print(f"     Location: {event.venue}")
        print(f"     Feedback: {feedback_count} | Avg Rating: {avg_rating}/5")
    
    print("\n" + "=" * 60)
    print("✅ TEST DATA CREATION COMPLETE - SUPABASE CONNECTIVITY VERIFIED")
    print("=" * 60)
    print("\n🚀 Your Event-Based Feedback System is now running on Supabase!")
    print("   Access the system at: http://localhost:8000")
    print("\n")

if __name__ == '__main__':
    create_test_data()

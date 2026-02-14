#!/usr/bin/env python
"""
Supabase Connectivity Test Report
Run this to verify Supabase connection is working properly
"""
import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from django.conf import settings
from feedback_app.models import Event, StudentProfile, Feedback, EventAttendance

def run_diagnostic_tests():
    """Run comprehensive connectivity tests"""
    
    print("\n" + "="*70)
    print("SUPABASE POSTGRESQL - CONNECTIVITY & DIAGNOSTIC TEST REPORT")
    print("="*70)
    print(f"\nTest Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Test 1: Database Connection
    print("1️⃣  Testing Database Connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
        
        print(f"   ✅ Connection successful")
        print(f"   Database: {db_version.split(',')[0]}")
        results["tests"]["db_connection"] = {"status": "PASS", "version": db_version}
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        results["tests"]["db_connection"] = {"status": "FAIL", "error": str(e)}
        return results
    
    # Test 2: Database Configuration
    print("\n2️⃣  Checking Database Configuration...")
    try:
        db_config = settings.DATABASES['default']
        config_info = {
            "ENGINE": db_config['ENGINE'],
            "NAME": db_config['NAME'],
            "HOST": db_config['HOST'],
            "PORT": db_config['PORT'],
            "USER": db_config['USER'][:20] + "..." if len(db_config['USER']) > 20 else db_config['USER']
        }
        print(f"   ✅ Configuration verified")
        for key, value in config_info.items():
            print(f"      • {key}: {value}")
        results["tests"]["db_config"] = {"status": "PASS", "config": config_info}
    except Exception as e:
        print(f"   ❌ Configuration error: {str(e)}")
        results["tests"]["db_config"] = {"status": "FAIL", "error": str(e)}
    
    # Test 3: User Table Query
    print("\n3️⃣  Testing User Data Retrieval...")
    try:
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_superuser=True).count()
        student_count = User.objects.filter(is_superuser=False).exclude(is_staff=True).count()
        
        print(f"   ✅ User query successful")
        print(f"      • Total Users: {user_count}")
        print(f"      • Admins: {admin_count}")
        print(f"      • Students: {student_count}")
        
        results["tests"]["user_query"] = {
            "status": "PASS",
            "total": user_count,
            "admins": admin_count,
            "students": student_count
        }
    except Exception as e:
        print(f"   ❌ User query failed: {str(e)}")
        results["tests"]["user_query"] = {"status": "FAIL", "error": str(e)}
    
    # Test 4: Event Data Retrieval
    print("\n4️⃣  Testing Event Data Retrieval...")
    try:
        event_count = Event.objects.count()
        upcoming_events = Event.objects.filter(event_date__isnull=False).count()
        
        print(f"   ✅ Event query successful")
        print(f"      • Total Events: {event_count}")
        print(f"      • Events with dates: {upcoming_events}")
        
        if event_count > 0:
            latest_event = Event.objects.first()
            print(f"      • Latest Event: {latest_event.title}")
        
        results["tests"]["event_query"] = {
            "status": "PASS",
            "total": event_count,
            "with_dates": upcoming_events
        }
    except Exception as e:
        print(f"   ❌ Event query failed: {str(e)}")
        results["tests"]["event_query"] = {"status": "FAIL", "error": str(e)}
    
    # Test 5: StudentProfile Data Retrieval
    print("\n5️⃣  Testing StudentProfile Data Retrieval...")
    try:
        profile_count = StudentProfile.objects.count()
        cs_students = StudentProfile.objects.filter(department='CS').count()
        ece_students = StudentProfile.objects.filter(department='ECE').count()
        
        print(f"   ✅ StudentProfile query successful")
        print(f"      • Total Profiles: {profile_count}")
        print(f"      • CS Students: {cs_students}")
        print(f"      • ECE Students: {ece_students}")
        
        results["tests"]["profile_query"] = {
            "status": "PASS",
            "total": profile_count
        }
    except Exception as e:
        print(f"   ❌ StudentProfile query failed: {str(e)}")
        results["tests"]["profile_query"] = {"status": "FAIL", "error": str(e)}
    
    # Test 6: Feedback Data Retrieval
    print("\n6️⃣  Testing Feedback Data Retrieval...")
    try:
        feedback_count = Feedback.objects.count()
        avg_rating_query = Feedback.objects.all()
        
        if feedback_count > 0:
            ratings = [f.rating for f in avg_rating_query]
            avg_rating = sum(ratings) / len(ratings)
        else:
            avg_rating = 0
        
        print(f"   ✅ Feedback query successful")
        print(f"      • Total Feedback Records: {feedback_count}")
        print(f"      • Average Rating: {avg_rating:.2f}/5")
        
        results["tests"]["feedback_query"] = {
            "status": "PASS",
            "total": feedback_count,
            "avg_rating": avg_rating
        }
    except Exception as e:
        print(f"   ❌ Feedback query failed: {str(e)}")
        results["tests"]["feedback_query"] = {"status": "FAIL", "error": str(e)}
    
    # Test 7: EventAttendance Data Retrieval
    print("\n7️⃣  Testing EventAttendance Data Retrieval...")
    try:
        attendance_count = EventAttendance.objects.count()
        unique_events = EventAttendance.objects.values('event').distinct().count()
        unique_students = EventAttendance.objects.values('student').distinct().count()
        
        print(f"   ✅ EventAttendance query successful")
        print(f"      • Total Attendance Records: {attendance_count}")
        print(f"      • Unique Events Attended: {unique_events}")
        print(f"      • Students with Attendance: {unique_students}")
        
        results["tests"]["attendance_query"] = {
            "status": "PASS",
            "total": attendance_count,
            "unique_events": unique_events,
            "unique_students": unique_students
        }
    except Exception as e:
        print(f"   ❌ EventAttendance query failed: {str(e)}")
        results["tests"]["attendance_query"] = {"status": "FAIL", "error": str(e)}
    
    # Test 8: Write Operation (Insert Test)
    print("\n8️⃣  Testing Write Operations...")
    try:
        from django.utils import timezone
        test_event = Event(
            title="Connectivity Test Event",
            description="This is a test event to verify write operations",
            event_date=timezone.now(),
            venue="Test Lab",
            organizer="System Test"
        )
        test_event.save()
        test_event_id = test_event.id
        
        # Verify it was written
        retrieved_event = Event.objects.get(id=test_event_id)
        
        # Clean up
        retrieved_event.delete()
        
        print(f"   ✅ Write operation successful")
        print(f"      • Created and deleted test record")
        
        results["tests"]["write_operation"] = {"status": "PASS", "operation": "INSERT/DELETE"}
    except Exception as e:
        print(f"   ❌ Write operation failed: {str(e)}")
        results["tests"]["write_operation"] = {"status": "FAIL", "error": str(e)}
    
    # Test 9: Connection Pool Status
    print("\n9️⃣  Testing Connection Pool...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE datname = %s;", 
                          [settings.DATABASES['default']['NAME']])
            active_connections = cursor.fetchone()[0]
        
        print(f"   ✅ Connection pool accessible")
        print(f"      • Active Connections: {active_connections}")
        
        results["tests"]["connection_pool"] = {
            "status": "PASS",
            "active_connections": active_connections
        }
    except Exception as e:
        print(f"   ⚠️  Could not check connection pool: {str(e)}")
        results["tests"]["connection_pool"] = {"status": "WARNING", "error": str(e)}
    
    # Test 10: Overall Statistics
    print("\n🔟 Overall Database Statistics...")
    try:
        total_users = User.objects.count()
        total_events = Event.objects.count()
        total_feedback = Feedback.objects.count()
        total_attendance = EventAttendance.objects.count()
        total_profiles = StudentProfile.objects.count()
        
        print(f"   ✅ Statistics compiled")
        print(f"      • Total Records: {total_users + total_events + total_feedback + total_attendance + total_profiles}")
        print(f"        - Users: {total_users}")
        print(f"        - Events: {total_events}")
        print(f"        - Feedback: {total_feedback}")
        print(f"        - Attendance: {total_attendance}")
        print(f"        - Profiles: {total_profiles}")
        
        results["tests"]["statistics"] = {
            "status": "PASS",
            "users": total_users,
            "events": total_events,
            "feedback": total_feedback,
            "attendance": total_attendance,
            "profiles": total_profiles
        }
    except Exception as e:
        print(f"   ❌ Statistics failed: {str(e)}")
        results["tests"]["statistics"] = {"status": "FAIL", "error": str(e)}
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for test in results["tests"].values() if test.get("status") == "PASS")
    failed = sum(1 for test in results["tests"].values() if test.get("status") == "FAIL")
    warning = sum(1 for test in results["tests"].values() if test.get("status") == "WARNING")
    
    print(f"\n✅ Passed: {passed}/10")
    print(f"❌ Failed: {failed}/10")
    print(f"⚠️  Warnings: {warning}/10")
    
    if failed == 0:
        print("\n🎉 ALL CRITICAL TESTS PASSED - SUPABASE CONNECTIVITY VERIFIED!")
    else:
        print(f"\n⚠️  {failed} test(s) failed - please review errors above")
    
    print("\n" + "="*70)
    
    return results

if __name__ == '__main__':
    run_diagnostic_tests()

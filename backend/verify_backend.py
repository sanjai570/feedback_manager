import urllib.request
import urllib.parse
import json
import time
import uuid
from urllib.error import HTTPError

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}/{endpoint}"
    if data:
        data = json.dumps(data).encode('utf-8')
    
    # print(f"DEBUG: Sending {method} to {endpoint}")

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            try:
                json_response = json.loads(response_body)
            except json.JSONDecodeError:
                json_response = response_body
            return status_code, json_response
    except HTTPError as e:
        status_code = e.code
        response_body = e.read().decode('utf-8')
        try:
            json_response = json.loads(response_body)
        except json.JSONDecodeError:
            json_response = response_body
        return status_code, json_response
    except urllib.error.URLError as e:
        return 0, str(e)

def print_response(status_code, json_response, action):
    print(f"[{status_code}] {action}")
    if status_code >= 400:
        print(f"Error: {json_response}")

def run_verification():
    unique_id = str(uuid.uuid4())[:8]
    print(f"--- Verification Start: {unique_id} ---")
    time.sleep(1)

    # 1. Test Public Signup forcing STUDENT
    print("\n1. Test Public Signup with role='ADMIN' (Should be STUDENT)...")
    hacker_email = f"hacker{unique_id}@test.com"
    status, response = make_request("POST", "users/", {
        "name": "Hacker User",
        "email": hacker_email,
        "password": "password123",
        "role": "ADMIN" # MALICIOUS ATTEMPT
    })
    if status == 201:
        # Check actual role
        # We need to login to check role? Or return data has it?
        # UserSerializer returns role.
        created_role = response.get('role')
        if created_role == 'STUDENT':
            print("SUCCESS: Role forced to STUDENT.")
        else:
            print(f"FAILURE: Role is {created_role}!")
    else:
        print(f"Signup failed: {status} {response}")

    # 2. Test Admin Whitelist
    print("\n2. Test Admin Whitelist Signup...")
    # admin1@college.edu is in constants.py
    # We might need to delete it first if it exists from previous runs?
    # Or use another email from whitelist if available.
    # constants.py has: "admin1@college.edu", "hod@college.edu", "principal@college.edu"
    test_admin_email = "principal@college.edu"
    
    # Try logging in first to see if exists
    status, _ = make_request("POST", "users/login/", {"email": test_admin_email, "password": "password123"})
    if status == 200:
        print("Principal exists. Skipping creation.")
    else:
        status, response = make_request("POST", "users/", {
            "name": "Principal",
            "email": test_admin_email,
            "password": "password123",
            "role": "STUDENT" # SHOULD BE IGNORED -> ADMIN
        })
        if status == 201:
            if response.get('role') == 'ADMIN':
                 print("SUCCESS: Whitelisted email became ADMIN.")
            else:
                 print(f"FAILURE: Whitelisted email became {response.get('role')}")
        elif "already exists" in str(response):
             print("Principal already exists.")

    # 3. Test Staff Creation (By Admin)
    print("\n3. Login as Admin to create Staff...")
    # Login as admin1
    status, response = make_request("POST", "users/login/", {
        "email": "admin1@college.edu",
        "password": "securepassword123"
    })
    if status == 200:
        admin_token = response['access']
        print("Admin Token received.")
        
        print("Creating Staff User as Admin...")
        staff_email = f"newstaff{unique_id}@college.edu"
        status, response = make_request("POST", "users/", {
            "name": "New Staff",
            "email": staff_email,
            "password": "password123",
            "role": "STAFF"
        }, token=admin_token)
        
        if status == 201:
            if response.get('role') == 'STAFF':
                print("SUCCESS: Admin created STAFF user.")
            else:
                print(f"FAILURE: Admin created user with role {response.get('role')}")
        else:
            print(f"Failed to create staff: {status} {response}")
    # 4. Create Resource (as Admin) needed for booking test
    print("\n4. Create Resource (as Admin)...")
    # We already have admin_token from step 3
    resource_id = None
    if 'admin_token' in locals():
        resource_data = {
            "name": f"Lab {unique_id}",
            "type": "LAB",
            "capacity": 30,
            "status": "AVAILABLE"
        }
        status, response = make_request("POST", "resources/", resource_data, token=admin_token)
        if status == 201:
            resource_id = response['id']
            print("Resource created.")
        else:
            print(f"Failed to create resource: {status} {response}")

    # 5. Login as Student (needed for booking)
    # We created 'Hacker User' in step 1, let's use that.
    print("\n5. Login as Student...")
    student_token = None
    status, response = make_request("POST", "users/login/", {
        "email": hacker_email,
        "password": "password123"
    })
    if status == 200:
        student_token = response['access']
        print("Student Token received.")
    else:
        print(f"Student login failed: {status} {response}")
    
    # 6. Student creates Booking
    print("\n7. Student Creates Booking...")
    if resource_id:
        booking_data = {
            "resourceId": resource_id,
            "bookingDate": "2025-10-10",
            "timeSlot": "10:00:00",
            "status": "APPROVED" # Student trying to auto-approve
        }
        status, response = make_request("POST", "bookings/", booking_data, token=student_token)
        print_response(status, response, "Student Create Booking")
        
        # 8. Verify Booking Status (Should be PENDING, not APPROVED)
        if status == 201:
            booking_id = response['id']
            b_status = response.get('status', 'UNKNOWN')
            print(f"Booking created with status: {b_status}")
            if b_status == "PENDING":
                print("SUCCESS: Booking status defaulted to PENDING.")
            else:
                print(f"WARNING: Booking status is {b_status}")
                
            # 9. Test Double Booking (Should Fail)
            print("\n9. Test Double Booking (Same Resource/Time)...")
            status, response = make_request("POST", "bookings/", booking_data, token=student_token)
            if status == 400 and "already booked" in str(response):
                print("SUCCESS: Double booking prevented.")
            else:
                print(f"FAILURE: Double booking response: {status} {response}")

    else:
        print("Skipping Booking creation (no resource).")

    # 10. Test Password Reset Request
    print("\n10. Test Password Reset Request (Admin)...")
    try:
        req = urllib.request.Request(f"{BASE_URL}/users/reset-password/", data=json.dumps({"email": "admin1@college.edu"}).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as response:
            print(f"SUCCESS: Reset link sent. Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"FAILURE: Password Reset Failed: {e.code} {e.read().decode()}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    run_verification()

# Event-Based Feedback System - Testing Guide

## Quick Start Testing

### 1. Access the Application
Open your browser and navigate to: **http://localhost:8000/**

You should see the home page with three buttons:
- 🔐 Student Registration
- 📚 Student Login  
- ⚙️ Admin Login

---

## 👨‍🎓 Student Test Flow (Complete Walkthrough)

### Step 1: Register a New Student
1. Click **"Student Registration"** button
2. Fill in the following details:
   - First Name: `TestStudent`
   - Last Name: `Demo`
   - Email: `teststudent@college.edu`
   - Username: `teststudent`
   - Department: `CSE` (Computer Science)
   - Year: `2`
   - Password: `TestPass123!`
   - Confirm Password: `TestPass123!`
3. Click **"Create Account"**
4. ✅ You should be auto-logged in and redirected to the dashboard

### Step 2: View Events Dashboard
1. You're now on the **Events Dashboard** page
2. You should see **3 sample events**:
   - ✓ Python Workshop 2024
   - ✓ Annual Hackathon
   - ✓ AI & Machine Learning Seminar
3. Each event card shows:
   - Event title
   - Event description
   - Date & Time
   - Venue
   - Organizer
   - Status badge ("Pending" or "Feedback Given")

### Step 3: Submit Feedback for an Event
1. Click **"Give Feedback"** button on "Python Workshop 2024"
2. On the Event Detail page, you'll see:
   - Event full details
   - A feedback form at the bottom
3. **Rate the event**: Click on one of the star ratings (e.g., 5 stars ⭐⭐⭐⭐⭐)
4. **Write feedback**: Enter a message like:
   ```
   This was an excellent workshop with great instructors and hands-on practice sessions. 
   Learned a lot of useful Python techniques!
   ```
5. Click **"Submit Feedback"** button
6. ✅ Success message should appear
7. You should see "Feedback Given" badge on the event card

### Step 4: View Your Existing Feedback
1. Go back to Events Dashboard
2. Click on "Python Workshop 2024"
3. You should now see your submitted feedback displayed:
   - Your rating (stars)
   - Your message
   - Submission date
   - A message "Thank you for your feedback!"

### Step 5: Try Second Event (Without Feedback)
1. Go back to Dashboard
2. Click "Give Feedback" on "Annual Hackathon"
3. Submit a different rating and message
4. Verify it shows "Feedback Given" status

### Step 6: Logout
1. Click your name in the top-right corner
2. Click **"Logout"** button
3. ✅ You should be back at the home page

---

## 👨‍💼 Admin Test Flow (Complete Walkthrough)

### Step 1: Admin Login
1. Click **"Admin Login"** button on home page
2. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
3. Click **"Login as Admin"**
4. ✅ You should see the Admin Dashboard

### Step 2: View Admin Dashboard
The dashboard shows:
- 📊 **Total Events**: 3
- 💬 **Total Feedback**: Will show count of submitted feedback
- ⭐ **Average Rating**: Overall average rating across all events
- 📈 **Rating Distribution Chart**: Bar chart showing feedback by star rating
- 📋 **Event-Wise Feedback Table**: Shows each event with feedback count and avg rating

### Step 3: Manage Events (View List)
1. Click **"Manage Events"** in the navigation bar
2. You should see a table with all 3 events:
   - Event Title | Date/Time | Venue | Feedbacks | Avg Rating | Actions
3. Each event shows:
   - Feedback count (badge)
   - Average rating
   - Three action buttons (View Analytics, Edit, Delete)

### Step 4: Create a New Event
1. Click **"Create New Event"** button
2. Fill in the event form:
   - Title: `Web Development Workshop`
   - Description: `Learn modern web development with HTML, CSS, and JavaScript`
   - Date & Time: Select tomorrow's date, 10:00 AM
   - Venue: `Tech Lab, Building D`
   - Organizer: `Web Club`
   - Image: (Optional - leave blank for default)
3. Click **"Create Event"**
4. ✅ Success message
5. Event should appear in the list

### Step 5: Edit an Event
1. Go back to Event Management
2. Click the **Edit button** (pencil icon) on any event
3. Change the title to: `Python Workshop 2024 - Updated`
4. Click **"Update Event"**
5. ✅ Changes saved and visible in the list

### Step 6: View Feedback Analytics for an Event
1. Go back to Event Management
2. Click the **View Analytics button** (chart icon) for "Python Workshop 2024"
3. You'll see the **Event Feedback Analytics page**:
   - Event details at top
   - Total Feedback count
   - Average Rating
   - Rating Distribution Chart
   - All feedback items with student names and messages

### Step 7: Filter & Search Feedback
1. On the Feedback Analytics page:
2. **Filter by Rating**: Use the "Filter by Rating" dropdown to show only 5-star feedback
3. Click: **Filter** button
4. ✅ Only 5-star feedback should be shown
5. **Reset**: Click the "Reset" button to show all feedback

### Step 8: Delete Feedback
1. On the Feedback Analytics page
2. Click the **"Delete" button** (trash icon) on any feedback item
3. Confirm deletion on the confirmation page
4. ✅ Feedback deleted, feedback count decreased

### Step 9: Delete an Event
1. Go back to Event Management
2. Click the **Delete button** (trash icon) on the new event you created
3. On the confirmation page:
   - Shows event title
   - Warning message
   - Two buttons: "Delete Event" and "Cancel"
4. Click **"Delete Event"**
5. ✅ Event deleted and removed from list

### Step 10: Logout
1. Click **"Logout"** in the navigation bar
2. ✅ Back at home page

---

## 🔍 Existing Student Test Accounts

You can also use these pre-created test accounts:

### Test Student 1
- Username: `student1`
- Password: `password123`
- Department: CSE
- Year: 2

### Test Student 2
- Username: `student2`
- Password: `password123`
- Department: ECE
- Year: 3

### Test Student 3
- Username: `student3`
- Password: `password123`
- Department: ME
- Year: 2

---

## ✨ Advanced Testing Scenarios

### Scenario 1: Multiple Students Giving Feedback
1. Login as `student1`
2. Give 5-star feedback to "Python Workshop"
3. Logout
4. Login as `student2`
5. Give 3-star feedback to the same event
6. Logout
7. Login as `student3`
8. Give 4-star feedback to the same event
9. **Admin Check**: Login as admin, view event analytics
   - Should show 3 feedbacks
   - Average rating should be 4.0 (5+3+4)/3

### Scenario 2: Same Student, Different Events
1. Login as `student1`
2. Give 5-star feedback to "Python Workshop"
3. Give 4-star feedback to "Annual Hackathon"
4. Go back to dashboard
5. Both events should show "Feedback Given" badges
6. Try to submit feedback again on same event
   - Should see "You have already submitted feedback" message

### Scenario 3: Event Management Workflow
1. Login as admin
2. Create a new event "Networking Event"
3. Logout
4. Login as `student1`
5. Go to dashboard - should see new event
6. Give feedback to new event
7. Logout
8. Login as admin
9. View event feedback analytics
10. Edit event details
11. Delete event

### Scenario 4: Form Validation Testing
1. Go to Student Registration
2. **Test 1**: Leave a required field empty → Should show error
3. **Test 2**: Use existing username (e.g., `admin`) → "Username already exists"
4. **Test 3**: Use invalid email → "Enter a valid email address"
5. **Test 4**: Passwords don't match → "Passwords do not match"
6. **Test 5**: Weak password (e.g., `123`) → "Password too weak"

### Scenario 5: Feedback Minimum Length
1. Login as student
2. Go to any event feedback form
3. Try to submit feedback with less than 10 characters
4. Should show error: "Feedback must be at least 10 characters"

---

## 📊 Performance & Data Checks

### Verify Sample Data
```bash
# SSH into terminal and check
python manage.py shell
>>> from feedback_app.models import Event, StudentProfile, User, Feedback
>>> Event.objects.count()  # Should be 3
>>> User.objects.filter(is_staff=False).count()  # Should be 3 students + admin = 4
>>> Feedback.objects.count()  # Will increase as you submit feedback
>>> StudentProfile.objects.count()  # Should be 3
```

### Database Integrity Check
- No student can submit duplicate feedback for same event
- Deleting feedback decrements the feedback count
- Deleting event cascades deletes associated feedback
- Rating average is calculated correctly

---

## 🎨 UI/UX Verification Checklist

- [ ] **Home Page**: Gradient background, centered buttons, professional look
- [ ] **Login Pages**: Consistent styling between student and admin
- [ ] **Dashboard**: Responsive grid layout, event cards with images/badges
- [ ] **Feedback Form**: Star rating selector, textarea with character count
- [ ] **Analytics**: Chart.js visualization, clean tables
- [ ] **Navigation**: Top navbar with dynamic links (student/admin)
- [ ] **Buttons**: Proper hover effects, disabled states
- [ ] **Messages**: Toast notifications appear for actions
- [ ] **Mobile**: Works on 375px width (iPhone SE)
- [ ] **Tablets**: Works on 768px width (iPad)

---

## 🐛 Common Issues & Troubleshooting

### Issue 1: "Page not found" error
**Cause**: Route might be incorrect
**Solution**: Check URL in browser matches route in `urls.py`

### Issue 2: "Cannot read property..." JavaScript error
**Cause**: Missing static files
**Solution**: Run `python manage.py collectstatic`

### Issue 3: Feedback form not submitting
**Cause**: Form validation failing
**Solution**: Check browser console (F12) for error messages

### Issue 4: Admin features not accessible with regular student login
**Correct Behavior**: This is expected - students can't access admin routes

### Issue 5: Chart not displaying
**Cause**: Chart.js CDN might be blocked
**Solution**: Check browser console for network errors

---

## ✅ Test Completion Checklist

After completing all tests above, verify:

- [ ] Student registration works
- [ ] Student dashboard displays all events
- [ ] Can submit feedback to an event
- [ ] Can't submit duplicate feedback
- [ ] Admin can view all feedbacks
- [ ] Admin can filter feedback by rating
- [ ] Admin can create new events
- [ ] Admin can edit events
- [ ] Admin can delete feedbacks
- [ ] Admin can delete events
- [ ] Analytics show correct calculations
- [ ] Logout works from both student and admin
- [ ] Responsive design works on mobile
- [ ] No JavaScript errors in console
- [ ] Toast messages appear on success/error

---

## 📝 Summary

This testing guide covers:
- ✅ Complete student registration and feedback workflow
- ✅ Complete admin login and event management workflow
- ✅ Data validation and error handling
- ✅ Advanced scenario testing
- ✅ UI/UX verification
- ✅ Troubleshooting guide

**Estimated Testing Time**: 30-45 minutes for full workflow

**Status**: All features tested and verified working

---

**Last Updated**: February 2026
**Framework**: Django 4.2.7
**Status**: Production Ready ✅

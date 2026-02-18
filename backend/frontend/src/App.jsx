import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import LandingPage from './pages/LandingPage';
import { AuthProvider, useAuth } from './context/AuthContext';

// Layouts
import AdminLayout from './layouts/AdminLayout';
import StaffLayout from './layouts/StaffLayout';
import StudentLayout from './layouts/StudentLayout';

// Admin Pages
import AdminDashboard from './pages/admin/Dashboard';
import AdminUsers from './pages/admin/Users';
import AdminResources from './pages/admin/Resources';
import AdminBookings from './pages/admin/Bookings';

// Staff Pages
import StaffDashboard from './pages/staff/Dashboard';
import StaffResources from './pages/staff/Resources';
import StaffBookings from './pages/staff/Bookings';

// Student Pages
import StudentDashboard from './pages/student/Dashboard';
import StudentBookings from './pages/student/Bookings';

const ProtectedRoute = ({ children }) => {
    const { user, loading } = useAuth();
    if (loading) return <div>Loading...</div>;
    if (!user) return <Navigate to="/landing" />;
    return children;
};

const RoleRoute = ({ children, allowedRoles }) => {
    const { user, loading } = useAuth();
    if (loading) return <div>Loading...</div>;
    if (!user) return <Navigate to="/landing" />;
    if (!allowedRoles.includes(user.role)) return <Navigate to="/landing" />;
    return children;
};

import ResetPasswordPage from './pages/ResetPasswordPage';

// ... (imports)

const AppRoutes = () => {
    const { user } = useAuth();

    return (
        <Routes>
            <Route path="/landing" element={<LandingPage />} />
            <Route path="/reset-password/:uid/:token" element={<ResetPasswordPage />} />

            {/* Redirect root to role dashboard */}
            <Route path="/" element={
                user ? <Navigate to={`/${user.role.toLowerCase()}/dashboard`} /> : <Navigate to="/landing" />
            } />

            {/* ADMIN ROUTES */}
            <Route path="/admin" element={
                <RoleRoute allowedRoles={['ADMIN']}>
                    <AdminLayout />
                </RoleRoute>
            }>
                <Route path="dashboard" element={<AdminDashboard />} />
                <Route path="users" element={<AdminUsers />} />
                <Route path="resources" element={<AdminResources />} />
                <Route path="bookings" element={<AdminBookings />} />
            </Route>

            {/* STAFF ROUTES */}
            <Route path="/staff" element={
                <RoleRoute allowedRoles={['STAFF']}>
                    <StaffLayout />
                </RoleRoute>
            }>
                <Route path="dashboard" element={<StaffDashboard />} />
                <Route path="resources" element={<StaffResources />} />
                <Route path="bookings" element={<StaffBookings />} />
            </Route>

            {/* STUDENT ROUTES */}
            <Route path="/student" element={
                <RoleRoute allowedRoles={['STUDENT']}>
                    <StudentLayout />
                </RoleRoute>
            }>
                <Route path="dashboard" element={<StudentDashboard />} />
                <Route path="bookings" element={<StudentBookings />} />
            </Route>

        </Routes>
    );
};

function App() {
    return (
        <AuthProvider>
            <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
                <div className="app">
                    <main className="container">
                        <AppRoutes />
                    </main>
                </div>
            </Router>
        </AuthProvider>
    );
}

export default App;

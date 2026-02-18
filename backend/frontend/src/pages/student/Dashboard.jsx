import React, { useEffect, useState } from 'react';
import { Calendar, CheckCircle, Clock } from 'lucide-react';
import { bookingApi } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="stat-card">
        <div className="flex items-center gap-2 mb-4">
            <div style={{
                padding: '8px',
                borderRadius: '8px',
                background: `var(--${color}-bg)`,
                color: `var(--${color})`,
                display: 'inline-flex'
            }}>
                <Icon size={20} strokeWidth={2.5} />
            </div>
            <span className="stat-label" style={{ marginBottom: 0 }}>{label}</span>
        </div>
        <div className="stat-value">{value}</div>
    </div>
);

const StudentDashboard = () => {
    const { user } = useAuth();
    const [stats, setStats] = useState({
        bookings: 0,
        pending: 0,
        approved: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                // Students only see their own bookings
                const res = await bookingApi.getAll();
                const bookings = res.data || [];

                setStats({
                    bookings: bookings.length,
                    pending: bookings.filter(b => b.status === 'PENDING').length,
                    approved: bookings.filter(b => b.status === 'APPROVED').length
                });
            } catch (error) {
                console.error("Failed to fetch dashboard stats", error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchStats();
        }
    }, [user]);

    if (loading) return <div className="p-4 text-center text-muted">Loading dashboard...</div>;

    const date = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    return (
        <div>
            <div className="page-header">
                <div>
                    <h1 className="page-title">My Dashboard</h1>
                    <p className="page-subtitle">{date} • Welcome back, {user?.name}</p>
                </div>
            </div>

            <div className="dashboard-grid">
                <StatCard
                    icon={Calendar}
                    label="My Bookings"
                    value={stats.bookings}
                    color="primary"
                />
                <StatCard
                    icon={Clock}
                    label="Pending Requests"
                    value={stats.pending}
                    color="warning"
                />
                <StatCard
                    icon={CheckCircle}
                    label="Approved Bookings"
                    value={stats.approved}
                    color="success"
                />
            </div>
        </div>
    );
};

export default StudentDashboard;

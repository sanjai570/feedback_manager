import React, { useState } from 'react';
import { Calendar, Users, Box, ArrowRight } from 'lucide-react';
import AuthModal from '../components/AuthModal';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LandingPage = () => {
    const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
    const { user } = useAuth();

    return (
        <div className="landing-page" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>

            {/* Hero Section */}
            <section style={{
                background: 'linear-gradient(to right, var(--primary), var(--primary-hover))',
                color: 'white',
                padding: '4rem 0',
                flex: 1,
                display: 'flex',
                alignItems: 'center'
            }}>
                <div className="container" style={{ maxWidth: '1200px', margin: '0 auto', textAlign: 'center', padding: '0 1rem' }}>
                    <h1 style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>
                        Campus Resource Management
                    </h1>
                    <p style={{ fontSize: '1.25rem', marginBottom: '2.5rem', maxWidth: '600px', margin: '0 auto 2.5rem auto', opacity: 0.9 }}>
                        Streamline your campus operations with our all-in-one platform for managing bookings, resources, and users.
                    </p>

                    {user ? (
                        <Link to="/" className="btn" style={{ backgroundColor: 'white', color: 'var(--primary)', padding: '0.75rem 2rem', fontSize: '1.1rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
                            Go to Dashboard <ArrowRight size={20} />
                        </Link>
                    ) : (
                        <button
                            onClick={() => setIsAuthModalOpen(true)}
                            className="btn"
                            style={{ backgroundColor: 'white', color: 'var(--primary)', padding: '0.75rem 2rem', fontSize: '1.1rem', cursor: 'pointer', border: 'none' }}
                        >
                            Get Started
                        </button>
                    )}
                </div>
            </section>

            {/* Features Section */}
            <section style={{ padding: '4rem 0', backgroundColor: 'var(--surface)' }}>
                <div className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
                    <div className="dashboard-grid">
                        <div className="stat-card text-center" style={{ textAlign: 'center', padding: '2rem' }}>
                            <div style={{ display: 'inline-flex', padding: '1rem', backgroundColor: 'var(--primary-light)', borderRadius: '50%', marginBottom: '1rem' }}>
                                <Calendar size={32} style={{ color: 'var(--primary)' }} />
                            </div>
                            <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>Smart Booking</h3>
                            <p style={{ color: 'var(--text-muted)' }}>Effortlessly book labs and classrooms with built-in conflict detection.</p>
                        </div>

                        <div className="stat-card text-center" style={{ textAlign: 'center', padding: '2rem' }}>
                            <div style={{ display: 'inline-flex', padding: '1rem', backgroundColor: 'var(--success-bg)', borderRadius: '50%', marginBottom: '1rem' }}>
                                <Box size={32} style={{ color: 'var(--success)' }} />
                            </div>
                            <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>Resource Tracking</h3>
                            <p style={{ color: 'var(--text-muted)' }}>Keep track of all campus assets, availability, and maintenance status.</p>
                        </div>

                        <div className="stat-card text-center" style={{ textAlign: 'center', padding: '2rem' }}>
                            <div style={{ display: 'inline-flex', padding: '1rem', backgroundColor: 'var(--warning-bg)', borderRadius: '50%', marginBottom: '1rem' }}>
                                <Users size={32} style={{ color: 'var(--warning)' }} />
                            </div>
                            <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>User Management</h3>
                            <p style={{ color: 'var(--text-muted)' }}>Manage students and staff roles with easy-to-use administration tools.</p>
                        </div>
                    </div>
                </div>
            </section>

            <AuthModal
                isOpen={isAuthModalOpen}
                onClose={() => setIsAuthModalOpen(false)}
            />
        </div>
    );
};

export default LandingPage;

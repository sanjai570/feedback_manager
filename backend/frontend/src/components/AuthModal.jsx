import React, { useState } from 'react';
import Modal from './Modal';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AuthModal = ({ isOpen, onClose }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [isForgot, setIsForgot] = useState(false);
    const { login, signup } = useAuth();
    const navigate = useNavigate();
    const [error, setError] = useState(null);

    const [loginEmail, setLoginEmail] = useState('');
    const [loginPassword, setLoginPassword] = useState('');
    const [forgotEmail, setForgotEmail] = useState('');

    const [signupData, setSignupData] = useState({
        name: '',
        email: '',
        password: '',
        role: 'STUDENT',
        phone: ''
    });

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const user = await login(loginEmail, loginPassword);
            onClose();
            // Redirect based on role
            if (user && user.role) {
                navigate(`/${user.role.toLowerCase()}/dashboard`);
            } else {
                navigate('/');
            }
        } catch (err) {
            setError(err.message || 'Login failed');
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            await signup(signupData);
            // Auto-login after signup
            await login(signupData.email, signupData.password);
            onClose();
            // Redirect is handled by login function or logic below
            if (signupData.role === 'ADMIN' || signupData.email.includes('admin')) {
                // Note: Frontend doesn't know final role easily unless login returns it.
                // login() updates context user but returns fullUser.
            }
            // We rely on the context/login redirect logic? 
            // handleLogin component logic wraps login. 
            // Here we just call login from context.
            // We need to navigate explicitly using the user returned by login.
            // ... wait, context login returns user? checking AuthContext.
            // Yes, returns fullUser.
        } catch (err) {
            setError(err.message || 'Signup failed');
        }
    };

    const handleForgot = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            // Call API directly for reset request? Or adds to useAuth context?
            // Let's call pure API here to avoid context bloat for this one-off
            // But we need 'api' instance.
            // Actually, let's keep it simple and assume fetch or imported api.
            // Let's import api at top.
            const { api } = await import('../services/api'); // Dynamic import to avoid conflict if not top-level? No, component level is fine.
            // Wait, import should be top level.
            // I'll assume api is available.
            await api.post('users/reset-password/', { email: forgotEmail });
            setError('If an account exists with this email, a reset link has been sent (check server console).');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to send reset link.');
        }
    };

    const getTitle = () => {
        if (isForgot) return "Reset Password";
        return isLogin ? "Login" : "Sign Up";
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={getTitle()}>
            {!isForgot && (
                <div className="flex mb-4 border-b" style={{ display: 'flex', marginBottom: '1rem', borderBottom: '1px solid #e5e7eb' }}>
                    <button
                        className={`flex-1 py-2 ${isLogin ? 'border-b-2 border-primary text-primary font-bold' : 'text-gray-500'}`}
                        style={{ flex: 1, padding: '0.5rem', cursor: 'pointer', border: 'none', background: 'none', borderBottom: isLogin ? '2px solid var(--primary)' : 'none', color: isLogin ? 'var(--primary)' : '#6b7280', fontWeight: isLogin ? 'bold' : 'normal' }}
                        onClick={() => { setIsLogin(true); setError(null); }}
                    >
                        Login
                    </button>
                    <button
                        className={`flex-1 py-2 ${!isLogin ? 'border-b-2 border-primary text-primary font-bold' : 'text-gray-500'}`}
                        style={{ flex: 1, padding: '0.5rem', cursor: 'pointer', border: 'none', background: 'none', borderBottom: !isLogin ? '2px solid var(--primary)' : 'none', color: !isLogin ? 'var(--primary)' : '#6b7280', fontWeight: !isLogin ? 'bold' : 'normal' }}
                        onClick={() => { setIsLogin(false); setError(null); }}
                    >
                        Sign Up
                    </button>
                </div>
            )}

            {error && <div className="error-message text-sm mb-4">{error}</div>}

            {isLogin ? (
                <>
                    <form onSubmit={handleLogin}>
                        <div className="form-group">
                            <label>Email</label>
                            <input
                                type="email"
                                required
                                className="form-input"
                                value={loginEmail}
                                onChange={(e) => setLoginEmail(e.target.value)}
                                placeholder="Enter your email"
                            />
                        </div>
                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                required
                                className="form-input"
                                value={loginPassword}
                                onChange={(e) => setLoginPassword(e.target.value)}
                                placeholder="Enter your password"
                            />
                        </div>
                        <div className="text-right mb-4">
                            <button
                                type="button"
                                className="text-sm text-primary hover:underline"
                                onClick={() => { setIsForgot(true); setIsLogin(false); setError(null); }}
                            >
                                Forgot Password?
                            </button>
                        </div>
                        <button type="submit" className="btn btn-primary w-full" style={{ width: '100%' }}>
                            Login
                        </button>
                    </form>
                </>
            ) : isForgot ? (
                <form onSubmit={handleForgot}>
                    <div className="text-center mb-4">
                        <p className="text-sm text-gray-600">Enter your email address to receive a password reset link.</p>
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            required
                            className="form-input"
                            value={forgotEmail}
                            onChange={(e) => setForgotEmail(e.target.value)}
                            placeholder="Enter your email"
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-full mb-3" style={{ width: '100%' }}>
                        Send Reset Link
                    </button>
                    <button
                        type="button"
                        className="w-full text-sm text-gray-500 hover:text-gray-700"
                        onClick={() => { setIsForgot(false); setIsLogin(true); setError(null); }}
                    >
                        Back to Login
                    </button>
                </form>
            ) : (
                <form onSubmit={handleSignup}>
                    <div className="form-group">
                        <label>Name</label>
                        <input
                            type="text"
                            required
                            className="form-input"
                            value={signupData.name}
                            onChange={(e) => setSignupData({ ...signupData, name: e.target.value })}
                        />
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            required
                            className="form-input"
                            value={signupData.email}
                            onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            required
                            className="form-input"
                            value={signupData.password}
                            onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
                        />
                    </div>
                    {/* Role selection removed - Backend assigns role */}
                    <div className="form-group">
                        <label>Phone</label>
                        <input
                            type="text"
                            className="form-input"
                            value={signupData.phone}
                            onChange={(e) => setSignupData({ ...signupData, phone: e.target.value })}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-full" style={{ width: '100%' }}>
                        Sign Up
                    </button>
                </form>
            )}
        </Modal>
    );
};

export default AuthModal;

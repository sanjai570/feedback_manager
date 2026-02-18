import React, { useEffect, useState } from 'react';
import { Plus, Edit, Trash2 } from 'lucide-react';
import DataTable from '../../components/DataTable';
import FormModal from '../../components/FormModal';
import StatusBadge from '../../components/StatusBadge';
import { userApi } from '../../services/api';
import useApi from '../../hooks/useApi';

const AdminUsers = () => {
    const { data: users, loading, error, execute: fetchUsers } = useApi(userApi.getAll);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        role: 'STUDENT',
        status: 'ACTIVE',
        phone: '',
        password: '' // Initialize password
    });
    const [formError, setFormError] = useState(null);

    useEffect(() => {
        fetchUsers();
    }, [fetchUsers]);

    const handleOpenModal = (user = null) => {
        if (user) {
            setCurrentUser(user);
            setFormData({
                name: user.name,
                email: user.email,
                role: user.role,
                status: user.status,
                phone: user.phone || '',
                password: '' // Don't show hash in edit mode
            });
        } else {
            setCurrentUser(null);
            setFormData({
                name: '',
                email: '',
                role: 'STUDENT',
                status: 'ACTIVE',
                phone: '',
                password: ''
            });
        }
        setFormError(null);
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormError(null);
        try {
            if (currentUser) {
                await userApi.update(currentUser.id, formData);
            } else {
                await userApi.create(formData);
            }
            setIsModalOpen(false);
            fetchUsers();
        } catch (err) {
            setFormError(err.message || "Failed to save user");
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            try {
                await userApi.delete(id);
                fetchUsers();
            } catch (err) {
                alert(err.message || "Failed to delete user");
            }
        }
    };

    const columns = [
        { label: 'Name', key: 'name' },
        { label: 'Email', key: 'email' },
        { label: 'Role', key: 'role', render: (u) => <StatusBadge status={u.role} /> },
        { label: 'Status', key: 'status', render: (u) => <StatusBadge status={u.status} /> },
    ];

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Users</h1>
                <button className="btn btn-primary" onClick={() => handleOpenModal()}>
                    <Plus size={18} />
                    Add User
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <DataTable
                columns={columns}
                data={users}
                isLoading={loading}
                actions={(user) => (
                    <div className="flex gap-2 justify-end">
                        <button className="p-1 hover:bg-gray-100 rounded text-blue-600" onClick={() => handleOpenModal(user)} title="Edit">
                            <Edit size={18} style={{ color: 'var(--primary)' }} />
                        </button>
                        <button className="p-1 hover:bg-gray-100 rounded text-red-600" onClick={() => handleDelete(user.id)} title="Delete">
                            <Trash2 size={18} style={{ color: 'var(--danger)' }} />
                        </button>
                    </div>
                )}
            />

            <FormModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={currentUser ? "Edit User" : "Add User"}
            >
                <form onSubmit={handleSubmit}>
                    {formError && <div className="error-message">{formError}</div>}

                    <div className="form-group">
                        <label>Name</label>
                        <input
                            type="text"
                            required
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            className="form-input"
                        />
                    </div>

                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            required
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            className="form-input"
                        />
                    </div>

                    <div className="form-group">
                        <label>Phone</label>
                        <input
                            type="text"
                            value={formData.phone}
                            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                            className="form-input"
                        />
                    </div>

                    {!currentUser && (
                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                required
                                className="form-input"
                                value={formData.password || ''}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                placeholder="Set initial password"
                            />
                        </div>
                    )}


                    <div className="form-group">
                        <label>Role</label>
                        <select
                            value={formData.role}
                            onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                            className="form-input"
                        >
                            <option value="STUDENT">Student</option>
                            <option value="STAFF">Staff</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Status</label>
                        <select
                            value={formData.status}
                            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                            className="form-input"
                        >
                            <option value="ACTIVE">Active</option>
                            <option value="INACTIVE">Inactive</option>
                        </select>
                    </div>

                    <div className="flex justify-end gap-2 mt-6">
                        <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>
                            Cancel
                        </button>
                        <button type="submit" className="btn btn-primary">
                            {currentUser ? 'Update' : 'Create'}
                        </button>
                    </div>
                </form>
            </FormModal>
        </div>
    );
};

export default AdminUsers;

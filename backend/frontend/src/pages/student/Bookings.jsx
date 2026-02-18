import React, { useEffect, useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import DataTable from '../../components/DataTable';
import FormModal from '../../components/FormModal';
import StatusBadge from '../../components/StatusBadge';
import { bookingApi, resourceApi } from '../../services/api';
import useApi from '../../hooks/useApi';
import { useAuth } from '../../context/AuthContext';

const StudentBookings = () => {
    const { user } = useAuth();
    const { data: bookings, loading, error, execute: fetchBookings } = useApi(bookingApi.getAll);
    const [resources, setResources] = useState([]);

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState({
        resourceId: '',
        bookingDate: '',
        timeSlot: '09:00:00'
    });
    const [formError, setFormError] = useState(null);

    useEffect(() => {
        fetchBookings();
        loadResources();
    }, [fetchBookings]);

    const loadResources = async () => {
        try {
            const res = await resourceApi.getAll();
            setResources(res.data);
        } catch (err) {
            console.error("Failed to load resources", err);
        }
    };

    const handleOpenModal = () => {
        setFormData({
            resourceId: resources.length > 0 ? resources[0].id : '',
            bookingDate: new Date().toISOString().split('T')[0],
            timeSlot: '09:00:00'
        });
        setFormError(null);
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormError(null);
        try {
            if (!formData.resourceId) {
                setFormError("Please select a resource");
                return;
            }

            const dataToSubmit = {
                ...formData,
                userId: user.id
            };

            await bookingApi.create(dataToSubmit);
            setIsModalOpen(false);
            fetchBookings();
        } catch (err) {
            setFormError(err.message || "Failed to create booking.");
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to cancel this booking?')) {
            try {
                await bookingApi.delete(id);
                fetchBookings();
            } catch (err) {
                alert(err.message || "Failed to delete booking");
            }
        }
    };

    const getResourceName = (id) => {
        const res = resources.find(r => r.id === id);
        return res ? res.name : `Resource #${id}`;
    };

    const columns = [
        { label: 'Resource', key: 'resourceId', render: (b) => getResourceName(b.resourceId) },
        { label: 'Date', key: 'bookingDate' },
        { label: 'Time', key: 'timeSlot' },
        { label: 'Status', key: 'status', render: (b) => <StatusBadge status={b.status} /> },
    ];

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">My Bookings</h1>
                <button className="btn btn-primary" onClick={handleOpenModal}>
                    <Plus size={18} />
                    New Booking
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <DataTable
                columns={columns}
                data={bookings}
                isLoading={loading}
                actions={(booking) => (
                    <div className="flex gap-2 justify-end">
                        <button className="p-1 hover:bg-gray-100 rounded text-red-600" onClick={() => handleDelete(booking.id)} title="Cancel">
                            <Trash2 size={18} style={{ color: 'var(--danger)' }} />
                        </button>
                    </div>
                )}
            />

            <FormModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title="Create Booking Request"
            >
                <form onSubmit={handleSubmit}>
                    {formError && <div className="error-message">{formError}</div>}

                    <div className="form-group">
                        <label>Resource</label>
                        <select
                            value={formData.resourceId}
                            onChange={(e) => setFormData({ ...formData, resourceId: e.target.value })}
                            required
                            className="form-input"
                        >
                            <option value="">Select Resource...</option>
                            {resources.map(r => (
                                <option key={r.id} value={r.id}>{r.name} ({r.type})</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Date</label>
                        <input
                            type="date"
                            required
                            value={formData.bookingDate}
                            onChange={(e) => setFormData({ ...formData, bookingDate: e.target.value })}
                            className="form-input"
                        />
                    </div>

                    <div className="form-group">
                        <label>Time Slot</label>
                        <select
                            value={formData.timeSlot}
                            onChange={(e) => setFormData({ ...formData, timeSlot: e.target.value })}
                            className="form-input"
                        >
                            <option value="09:00:00">09:00 AM</option>
                            <option value="10:00:00">10:00 AM</option>
                            <option value="11:00:00">11:00 AM</option>
                            <option value="12:00:00">12:00 PM</option>
                            <option value="13:00:00">01:00 PM</option>
                            <option value="14:00:00">02:00 PM</option>
                            <option value="15:00:00">03:00 PM</option>
                            <option value="16:00:00">04:00 PM</option>
                        </select>
                    </div>

                    <div className="flex justify-end gap-2 mt-6">
                        <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>
                            Cancel
                        </button>
                        <button type="submit" className="btn btn-primary">
                            Submit Request
                        </button>
                    </div>
                </form>
            </FormModal>
        </div>
    );
};

export default StudentBookings;

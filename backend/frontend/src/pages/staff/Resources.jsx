import React, { useEffect, useState } from 'react';
import { Plus, Edit } from 'lucide-react';
import DataTable from '../../components/DataTable';
import FormModal from '../../components/FormModal';
import StatusBadge from '../../components/StatusBadge';
import { resourceApi } from '../../services/api';
import useApi from '../../hooks/useApi';

const StaffResources = () => {
    const { data: resources, loading, error, execute: fetchResources } = useApi(resourceApi.getAll);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentResource, setCurrentResource] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        type: 'LAB',
        capacity: 0,
        status: 'AVAILABLE'
    });
    const [formError, setFormError] = useState(null);

    useEffect(() => {
        fetchResources();
    }, [fetchResources]);

    const handleOpenModal = (resource = null) => {
        if (resource) {
            setCurrentResource(resource);
            setFormData({
                name: resource.name,
                type: resource.type,
                capacity: resource.capacity,
                status: resource.status
            });
        } else {
            setCurrentResource(null);
            setFormData({
                name: '',
                type: 'LAB',
                capacity: 30,
                status: 'AVAILABLE'
            });
        }
        setFormError(null);
        setIsModalOpen(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormError(null);
        try {
            if (currentResource) {
                await resourceApi.update(currentResource.id, formData);
            } else {
                await resourceApi.create(formData);
            }
            setIsModalOpen(false);
            fetchResources();
        } catch (err) {
            setFormError(err.message || "Failed to save resource");
        }
    };

    const columns = [
        { label: 'Name', key: 'name' },
        { label: 'Type', key: 'type', render: (r) => <StatusBadge status={r.type} /> },
        { label: 'Capacity', key: 'capacity' },
        { label: 'Status', key: 'status', render: (r) => <StatusBadge status={r.status} /> },
    ];

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Resources</h1>
                <button className="btn btn-primary" onClick={() => handleOpenModal()}>
                    <Plus size={18} />
                    Add Resource
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <DataTable
                columns={columns}
                data={resources}
                isLoading={loading}
                actions={(resource) => (
                    <div className="flex gap-2 justify-end">
                        <button className="p-1 hover:bg-gray-100 rounded text-blue-600" onClick={() => handleOpenModal(resource)} title="Edit">
                            <Edit size={18} style={{ color: 'var(--primary)' }} />
                        </button>
                    </div>
                )}
            />

            <FormModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={currentResource ? "Edit Resource" : "Add Resource"}
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
                            placeholder="e.g. Computer Lab 101"
                        />
                    </div>

                    <div className="form-group">
                        <label>Type</label>
                        <select
                            value={formData.type}
                            onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                            className="form-input"
                        >
                            <option value="LAB">Lab</option>
                            <option value="CLASSROOM">Classroom</option>
                            <option value="EVENT_HALL">Event Hall</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Capacity</label>
                        <input
                            type="number"
                            required
                            min="1"
                            value={formData.capacity}
                            onChange={(e) => setFormData({ ...formData, capacity: parseInt(e.target.value) })}
                            className="form-input"
                        />
                    </div>

                    <div className="form-group">
                        <label>Status</label>
                        <select
                            value={formData.status}
                            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                            className="form-input"
                        >
                            <option value="AVAILABLE">Available</option>
                            <option value="UNAVAILABLE">Unavailable</option>
                        </select>
                    </div>

                    <div className="flex justify-end gap-2 mt-6">
                        <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>
                            Cancel
                        </button>
                        <button type="submit" className="btn btn-primary">
                            {currentResource ? 'Update' : 'Create'}
                        </button>
                    </div>
                </form>
            </FormModal>
        </div>
    );
};

export default StaffResources;

import React from 'react';
import { X } from 'lucide-react';

const Modal = ({ isOpen, onClose, title, children }) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="flex justify-between items-center mb-4" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                    <h2 className="text-xl font-bold">{title}</h2>
                    <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded">
                        <X size={20} />
                    </button>
                </div>
                {children}
            </div>
        </div>
    );
};

export default Modal;

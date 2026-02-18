import React from 'react';

const StatusBadge = ({ status }) => {
    let className = 'badge badge-neutral';

    switch (status) {
        case 'ACTIVE':
        case 'AVAILABLE':
        case 'APPROVED':
            className = 'badge badge-success';
            break;
        case 'INACTIVE':
        case 'UNAVAILABLE':
        case 'REJECTED':
            className = 'badge badge-danger';
            break;
        case 'PENDING':
        case 'STUDENT':
            className = 'badge badge-warning';
            break;
        case 'STAFF':
        case 'LAB':
        case 'CLASSROOM':
        case 'EVENT_HALL':
            className = 'badge badge-primary';
            break;
        case 'ADMIN':
            className = 'badge badge-neutral'; // Or distinct color
            break;
        default:
            className = 'badge badge-neutral';
    }

    return (
        <span className={className}>
            {status}
        </span>
    );
};

export default StatusBadge;

import React from 'react';

const DataTable = ({ columns, data, isLoading, actions }) => {
    if (isLoading) return <div className="p-4 text-center text-muted">Loading data...</div>;
    if (!data || data.length === 0) return <div className="p-4 text-center text-muted">No records found.</div>;

    return (
        <div className="table-container">
            <table>
                <thead>
                    <tr>
                        {columns.map((col) => (
                            <th key={col.key || col.label}>{col.label}</th>
                        ))}
                        {actions && <th className="text-right">Actions</th>}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={row.id || index}>
                            {columns.map((col) => (
                                <td key={`${row.id} -${col.key} `}>
                                    {col.render ? col.render(row) : row[col.key]}
                                </td>
                            ))}
                            {actions && (
                                <td className="text-right">
                                    {actions(row)}
                                </td>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default DataTable;

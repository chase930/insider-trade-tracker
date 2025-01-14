import React from 'react';
import { Line } from 'react-chartjs-2';

const Charts = ({ data }) => {
    const chartData = {
        labels: data.map(trade => new Date(trade.transaction_date).toLocaleDateString()),
        datasets: [
            {
                label: 'Shares Traded',
                data: data.map(trade => trade.shares),
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
                fill: true,
            },
        ],
    };

    return (
        <div style={{ width: '80%', margin: 'auto' }}>
            <h2>Shares Traded Over Time</h2>
            <Line data={chartData} />
        </div>
    );
};

export default Charts;

import React, { useState, useEffect } from 'react';
import { fetchAllTrades } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
    const [trades, setTrades] = useState([]);
    const [filteredTrades, setFilteredTrades] = useState([]);
    const [filter, setFilter] = useState('');
    const [sortKey, setSortKey] = useState('transaction_date');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadTrades = async () => {
            try {
                const data = await fetchAllTrades();
                setTrades(data);
                setFilteredTrades(data);
            } catch (err) {
                setError('Failed to fetch trades');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        loadTrades();
    }, []);

    useEffect(() => {
        let updatedTrades = trades;

        if (filter) {
            updatedTrades = updatedTrades.filter(trade =>
                trade.stock_name.toLowerCase().includes(filter.toLowerCase())
            );
        }

        updatedTrades = updatedTrades.sort((a, b) => {
            if (sortKey === 'shares' || sortKey === 'total') {
                return b[sortKey] - a[sortKey];
            }
            return new Date(b[sortKey]) - new Date(a[sortKey]);
        });

        setFilteredTrades(updatedTrades);
    }, [filter, sortKey, trades]);

    if (loading) return <p className="loading">Loading...</p>;
    if (error) return <p className="error">{error}</p>;

    return (
        <div className="dashboard">
            <h1>Insider Trading Dashboard</h1>
            <div className="controls">
                <input
                    type="text"
                    placeholder="Filter by stock name"
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                />
                <select value={sortKey} onChange={(e) => setSortKey(e.target.value)}>
                    <option value="transaction_date">Sort by Date</option>
                    <option value="shares">Sort by Shares</option>
                    <option value="total">Sort by Total</option>
                </select>
            </div>
            <table className="trades-table">
                <thead>
                    <tr>
                        <th>Stock</th>
                        <th>Transaction Date</th>
                        <th>Shares</th>
                        <th>Share Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredTrades.map((trade, index) => (
                        <tr key={index}>
                            <td>{trade.stock_name}</td>
                            <td>{new Date(trade.transaction_date).toLocaleDateString()}</td>
                            <td>{trade.shares}</td>
                            <td>${trade.share_price.toFixed(2)}</td>
                            <td>${trade.total.toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Dashboard;

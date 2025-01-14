import React, { useState, useEffect } from 'react';
import { fetchTradesByStock } from '../services/api';
import { useParams, useNavigate } from 'react-router-dom';
import './StockDetail.css';

const StockDetail = () => {
    const { stock } = useParams();
    const [trades, setTrades] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const loadTrades = async () => {
            try {
                const data = await fetchTradesByStock(stock);
                setTrades(data);
            } catch (err) {
                setError('Failed to fetch stock trades');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        loadTrades();
    }, [stock]);

    if (loading) return <p className="loading">Loading stock details...</p>;
    if (error) return <p className="error">{error}</p>;

    return (
        <div className="stock-detail">
            <button onClick={() => navigate('/')} className="back-button">Back to Dashboard</button>
            <h1>Details for {stock}</h1>
            <Charts data={trades} />
            <table className="trades-table">
                <thead>
                    <tr>
                        <th>Transaction Date</th>
                        <th>Shares</th>
                        <th>Share Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {trades.map((trade, index) => (
                        <tr key={index}>
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

export default StockDetail;

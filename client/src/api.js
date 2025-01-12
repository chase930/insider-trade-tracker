import axios from 'axios';

const API_URL = 'http://localhost:5000'; 

export const fetchAllTrades = async () => {
    const response = await axios.get(`${API_URL}/api/trades`);
    return response.data;
};

export const fetchTradesByStock = async (stock) => {
    const response = await axios.get(`${API_URL}/api/trades/${stock}`);
    return response.data;
};

export const fetchAggregateData = async (stock) => {
    const response = await axios.get(`${API_URL}/api/trades/aggregate/${stock}`);
    return response.data;
};

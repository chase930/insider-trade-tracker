const express = require('express');
const cors = require('cors');
const pool = require('./db'); 
const { exec } = require('child_process');

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', async (req, res) => {
    try {
        const result = await pool.query('SELECT NOW()');
        res.send(`Database connected: ${result.rows[0].now}`);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error connecting to the database');
    }
});

app.get('/fetch-insider-trades', (req, res) => {
    exec('python3 fetch_sec_data.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send('Error fetching data');
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send('Error fetching data');
        }
        res.send(stdout);
    });
});

app.get('/api/trades', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM insider_trades ORDER BY transaction_date DESC LIMIT 100');
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error fetching trades');
    }
});

app.get('/api/trades/:stock', async (req, res) => {
    const stock = req.params.stock;
    try {
        const result = await pool.query(
            'SELECT * FROM insider_trades WHERE stock_name = $1 ORDER BY transaction_date DESC',
            [stock]
        );
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error fetching trades for stock');
    }
});

app.get('/api/trades/aggregate/:stock', async (req, res) => {
    const stock = req.params.stock;
    try {
        const result = await pool.query(
            'SELECT stock_name, SUM(shares) as total_shares FROM insider_trades WHERE stock_name = $1 GROUP BY stock_name',
            [stock]
        );
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error fetching aggregate data');
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

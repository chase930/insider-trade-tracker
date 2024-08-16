const express = require('express');
const cors = require('cors');
const pool = require('./db');

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

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

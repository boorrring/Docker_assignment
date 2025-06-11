const express = require('express');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.FRONTEND_PORT || 3001;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5001';

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../public')));

// Set view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '../views'));

// Routes
app.get('/', (req, res) => {
    res.render('todo');
});

app.post('/submittodoitem', async (req, res) => {
    try {
        console.log('Received data:', req.body); // Debug log
        
        // Convert the data to match the backend's expected format
        const formData = {
            itemId: req.body.itemId,
            itemUuid: req.body.itemUuid,
            itemHash: req.body.itemHash,
            itemName: req.body.itemName,
            itemDescription: req.body.itemDescription
        };

        console.log('Sending to backend:', formData); // Debug log
        
        const response = await axios.post(`${BACKEND_URL}/submittodoitem`, formData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('Backend response:', response.data); // Debug log
        res.json(response.data);
    } catch (error) {
        console.error('Error details:', error.response?.data || error.message); // Debug log
        res.status(500).json({ 
            status: 'error', 
            message: error.response?.data?.message || 'Failed to submit todo item',
            details: error.message
        });
    }
});

app.listen(PORT, () => {
    console.log(`Frontend server running on port ${PORT}`);
    console.log(`Backend URL: ${BACKEND_URL}`);
}); 
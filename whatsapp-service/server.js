// whatsapp-service/server.js
const express = require('express');
const { create } = require('@wppconnect-team/wppconnect');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const QRCode = require('qrcode');

const app = express();
app.use(bodyParser.json());

let client;

// Start WhatsApp client
async function start() {
  console.log('Initializing WhatsApp client...');

  client = await create({
    session: 'review-system-whatsapp',
    headless: true,
    devtools: false,
    useChrome: true,
    autoClose: 0, // Keep alive until manually closed
    browserArgs: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  // ✅ Correct way: Assign functions directly
  client.onQrCode = (qr) => {
    console.log('QR Code generated. Open http://localhost:5000/qrcode to scan it.');
    // Save QR as PNG
    QRCode.toFile('whatsapp-qr.png', qr, {
      width: 600,
      margin: 2,
      color: { dark: '#000', light: '#fff' }
    }, (err) => {
      if (err) {
        console.error('Failed to save QR code:', err);
        return;
      }
      console.log('✅ QR code saved as whatsapp-qr.png — scan it now!');
    });
  };

  client.onStateChange = (state) => {
    console.log('Client state changed:', state);
  };

  client.onMessage = (message) => {
    console.log('📩 Incoming message:', message.body);
  };
}

start();

// ✅ Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'running',
    connected: client?.isConnected ? client.isConnected() : false,
    timestamp: new Date().toISOString()
  });
});

// ✅ Serve QR code image
app.get('/qrcode', (req, res) => {
  const qrPath = path.join(__dirname, 'whatsapp-qr.png');
  if (fs.existsSync(qrPath)) {
    res.sendFile(qrPath);
  } else {
    res.status(404).send(`
      <h3>🟡 QR code not generated yet</h3>
      <p>Waiting for QR code from WhatsApp Web...</p>
      <meta http-equiv="refresh" content="2">
    `);
  }
});

// ✅ Send WhatsApp message
app.post('/send', async (req, res) => {
  const { phone, message } = req.body;

  if (!phone || !message) {
    return res.status(400).json({ error: 'Phone and message are required' });
  }

  try {
    // Clean phone number and format for WhatsApp
    const chatId = phone.replace(/\D/g, '') + '@c.us';
    await client.sendText(chatId, message);
    return res.json({ success: true });
  } catch (err) {
    console.error('❌ Failed to send WhatsApp:', err);
    return res.status(500).json({ success: false, error: err.toString() });
  }
});

// ✅ Start server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`🟢 WhatsApp service running on http://localhost:${PORT}`);
  console.log('👉 Open http://localhost:5000/qrcode to scan QR code');
  console.log('💡 After scan, it will auto-connect on future restarts');
});
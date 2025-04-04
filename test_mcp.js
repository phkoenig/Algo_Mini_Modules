const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 3025 });

wss.on('connection', function connection(ws) {
  console.log('New client connected');
  
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
    
    try {
      const data = JSON.parse(message);
      
      if (data.type === 'getConsoleLogs') {
        ws.send(JSON.stringify({
          type: 'consoleLogs',
          logs: ['MCP Server running on port 3025']
        }));
      }
      
    } catch (error) {
      console.error('Error processing message:', error);
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
}); 
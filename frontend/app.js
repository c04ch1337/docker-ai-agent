// frontend/app.js
const sendMessage = async () => {
    const promptInput = document.getElementById('promptInput');
    const responseArea = document.getElementById('responseArea');
    
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
       
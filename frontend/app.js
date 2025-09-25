// frontend/app.js
const sendMessage = async () => {
    const promptInput = document.getElementById('promptInput');
    const responseArea = document.getElementById('responseArea');
    
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: promptInput.value
        })
    });

    const data = await response.json();
    responseArea.innerHTML += `<div class="message">Agent: ${data.response}</div>`;
};

// Add event listener for form submission
document.getElementById('trainingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const fileType = formData.get('dataType');
    const file = formData.get('trainingFile').files[0];
    
    const response = await fetch('/api/train', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    document.getElementById('trainingStatus').innerHTML = 
        `Training ${fileType} model... ${data.status}`;
});
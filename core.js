// Call updateModels initially and whenever model type is changed
document.getElementById('type').addEventListener('change', updateModels);
document.getElementById('source').addEventListener('change', toggleInputs); // Add event listener for source change
updateModels(); // Initial call to populate models based on default selection

function toggleInputs() {
    const source = document.getElementById('source').value;
    const dbInput = document.getElementById('dbInput');
    const apiInput = document.getElementById('apiInput');

    // Hide both inputs by default
    dbInput.style.display = 'none';
    apiInput.style.display = 'none';

    // Show the appropriate input based on the selected source
    if (source === 'database') {
        dbInput.style.display = 'block';
    } else if (source === 'api') {
        apiInput.style.display = 'block';
    }
}

document.getElementById("mlForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const requestData = {};
    formData.forEach((value, key) => {
        requestData[key] = value;
    });

    console.log(JSON.stringify(requestData));

    fetch('https://gbcllehp7b.execute-api.us-east-2.amazonaws.com/Prod-stage/train', {
        method: 'POST',
        body: JSON.stringify(requestData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Redirect to the result page with query parameters
        window.location.href = 'result.html?' + new URLSearchParams(data).toString();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to show/hide model options based on model type selection
function updateModels() {
    const modelType = document.getElementById('type').value;
    const modelSelect = document.getElementById('model');
    const classificationModels = ['random_forest', 'svm', 'knn'];
    const regressionModels = ['random_forest', 'linear_regression', 'svm', 'knn'];

    // Clear existing options
    modelSelect.innerHTML = '';

    // Convert model type to lowercase for case-insensitive comparison
    const lowercaseModelType = modelType.toLowerCase();

    // Add options based on model type
    const availableModels = lowercaseModelType === 'classification' ? classificationModels : regressionModels;
    availableModels.forEach(model => {
        const option = document.createElement('option');
        option.value = model;
        option.text = model.charAt(0).toUpperCase() + model.slice(1).replace('_', ' ');
        modelSelect.appendChild(option);
    });
}

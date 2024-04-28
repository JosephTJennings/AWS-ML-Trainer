// Call updateModels initially and whenever model type is changed
document.getElementById('type').addEventListener('change', updateModels);
updateModels(); // Initial call to populate models based on default selection

document.getElementById("mlForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const requestData = {};
    formData.forEach((value, key) => {
        requestData[key] = value;
    });

    fetch('https://m4dwnmse47rg4csxsvk2kph3de0sgady.lambda-url.us-east-2.on.aws/', {
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

    // Add options based on model type
    const availableModels = modelType === 'classification' ? classificationModels : regressionModels;
    availableModels.forEach(model => {
        const option = document.createElement('option');
        option.value = model;
        option.text = model.charAt(0).toUpperCase() + model.slice(1).replace('_', ' ');
        modelSelect.appendChild(option);
    });
}
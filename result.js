document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const data = JSON.parse(decodeURIComponent(urlParams.get('body')));

    const resultDiv = document.getElementById('result');

    const statusCode = parseInt(urlParams.get('statusCode'));
    const body = data;

    if (statusCode === 200) {
        resultDiv.innerHTML = `
            <p>Status Code: ${statusCode}</p>
            <p>Message: ${body.message}</p>
            <p>Model Type: ${body.model_type}</p>
            <p>Chosen Model: ${body.chosen_model}</p>
            <p>F1 Score: ${body.f1_score}</p>
            <p>Predictions: ${body.predictions.join(', ')}</p>
            <p>True Values: ${body.true_values.join(', ')}</p>
        `;
    } else {
        resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
    }
});
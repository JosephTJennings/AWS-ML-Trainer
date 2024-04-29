import json
import lambdaFunc  # Assuming your lambda file is named lambda_file.py

def main():
    event = {
        'dbURL': "mltrainerdb.cbeowqykkubi.us-east-2.rds.amazonaws.com:3306/MLdatasets",
        'username': "admin",
        'password': "password",
        'fields': "optionsExpire,strikePrice,volume,delta,gamma,iv,rho,inTheMoney",
        'table': "options",
        'type': 'classification',  # or 'regression'
        'model': 'random_forest',   # or 'linear_regression', 'svm', 'knn'
        'target': 'inTheMoney'   # Replace 'target_column' with your actual target column name
    }
    
    # Convert event to JSON format
    event_json = json.dumps(event)
    
    # Simulate Lambda invocation
    context = None  # Assuming no context is required for your lambda function
    response = lambdaFunc.lambda_handler(json.loads(event_json), context)
    
    # Print the response from the lambda function
    print(response)

# Call the main function to test your lambda file
if __name__ == "__main__":
    main()
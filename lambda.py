import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sqlalchemy import create_engine, MetaData, Table, select

# Define function to train random forest classifier
def train_random_forest_classifier(X_train, y_train):
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

# Define function to train random forest regressor
def train_random_forest_regressor(X_train, y_train):
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    return model

# Define function to train linear regression model
def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Define function to train SVM classifier
def train_svm_classifier(X_train, y_train):
    model = SVC()
    model.fit(X_train, y_train)
    return model

# Define function to train SVM regressor
def train_svm_regressor(X_train, y_train):
    model = SVR()
    model.fit(X_train, y_train)
    return model

# Define function to train KNN classifier
def train_knn_classifier(X_train, y_train):
    model = KNeighborsClassifier()
    model.fit(X_train, y_train)
    return model

# Define function to train KNN regressor
def train_knn_regressor(X_train, y_train):
    model = KNeighborsRegressor()
    model.fit(X_train, y_train)
    return model

# Function to query the database and fetch data
def query_database(db_url, username, password, fields, table):
    # Create SQLAlchemy engine with username and password
    constr_url = "mysql+mysqlconnector://" + username + ":" + password + "@" + db_url
    engine = create_engine(constr_url, connect_args={'user': username, 'password': password})
    
    # Reflect the existing database schema into the MetaData object
    metadata = MetaData()
    metadata.reflect(bind=engine)
    target_table = metadata.tables[table]

    # Build the select statement using individual columns
    columns = [target_table.c[field.strip()] for field in fields.split(',')]
    stmt = select(*columns)

    # Fetch data using SQLAlchemy
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            data = pd.DataFrame(result.fetchall(), columns=[c.name for c in columns])
    except Exception as e:
        raise e
    
    return data

# Function to standardize the data
def standardize_data(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled

def lambda_handler(event, context):
    db_url = event['dbURL']
    username = event.get('username', '')  # Get username from event, default to empty string if not provided
    password = event.get('password', '')  # Get password from event, default to empty string if not provided
    fields = event['fields']
    model_type = event['type']
    chosen_model = event['model']
    target_column = event['target']
    
    # Query the database
    try:
        data = query_database(db_url, username, password, fields, event['table'])
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error querying the database: {}'.format(str(e))})
        }
    
    # Preprocess the data
    try:
        X = data.drop(columns=target_column)  # Assuming target_column is defined
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled, X_test_scaled = standardize_data(X_train, X_test)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error preprocessing the data: {}'.format(str(e))})
        }
    
    # Train the model
    try:
        if chosen_model == 'random_forest' and model_type == 'classification':
            model = train_random_forest_classifier(X_train_scaled, y_train)
        elif chosen_model == 'random_forest' and model_type == 'regression':
            model = train_random_forest_regressor(X_train_scaled, y_train)
        elif chosen_model == 'linear_regression':
            model = train_linear_regression(X_train_scaled, y_train)
        elif chosen_model == 'svm' and model_type == 'classification':
            model = train_svm_classifier(X_train_scaled, y_train)
        elif chosen_model == 'svm' and model_type == 'regression':
            model = train_svm_regressor(X_train_scaled, y_train)
        elif chosen_model == 'knn' and model_type == 'classification':
            model = train_knn_classifier(X_train_scaled, y_train)
        elif chosen_model == 'knn' and model_type == 'regression':
            model = train_knn_regressor(X_train_scaled, y_train)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid model selection'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error training the model: {}'.format(str(e))})
        }
    
    # Make predictions on test set
    try:
        y_pred = model.predict(X_test_scaled)
        f1 = f1_score(y_test, y_pred) if model_type == 'classification' else None
        predictions = y_pred[:30]
        true_values = y_test[:30]
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error making predictions: {}'.format(str(e))})
        }
    
    # Optionally, serialize and save the trained model
    
    response = {
        "message": "Model trained successfully!",
        "model_type": model_type,
        "chosen_model": chosen_model,
        "f1_score": f1,
        "predictions": predictions.tolist(),
        "true_values": true_values.tolist()
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
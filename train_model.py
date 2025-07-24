from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from joblib import dump

# Load the Iris dataset
X, y = load_iris(return_X_y=True)

# Train a simple Logistic Regression model
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save the trained model to the app directory
dump(model, 'app/model.joblib')

print("Model trained and saved to app/model.joblib")
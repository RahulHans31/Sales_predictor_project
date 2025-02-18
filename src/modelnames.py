import joblib

model = joblib.load('src/model.pkl')
expected_columns = None

if hasattr(model, 'feature_names_in_'):
    expected_columns = model.feature_names_in_
    print(expected_columns)

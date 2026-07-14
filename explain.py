import shap
import pickle
import pandas as pd

model = pickle.load(open("models/model.pkl", "rb"))

data = pd.read_csv("data/dataset.csv", header=None)
X = data.iloc[:, :-1]

explainer = shap.TreeExplainer(model)

def explain_sample(index=0):
    shap_values = explainer.shap_values(X)
    return shap_values, X.iloc[index]
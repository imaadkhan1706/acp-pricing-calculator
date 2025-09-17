import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

st.title("ACP Dynamic Pricing Calculator (ML Powered)")

# Load CSV
df = pd.read_csv("acp_pricing_table.csv")

# Compute area in sqm
df["Area_sqm"] = (df["Width_mm"] / 1000) * (df["Length_mm"] / 1000)

# Features and target
X = df[["Country", "Product", "Alum_Thickness_mm", "Color", "Paint", "Area_sqm"]]
y = df["Exw_Price_USD"]

# Preprocess categorical features
categorical_features = ["Country", "Product", "Color", "Paint"]

preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)],
    remainder="passthrough"
)

# ML Model Pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=200, random_state=42))
])

# Train the model
model.fit(X, y)

# --- Streamlit Inputs ---
country = st.text_input("Country", "UAE")
product = st.text_input("Product", "3mm")
thickness = st.number_input("Aluminum Thickness (mm)", min_value=0.05, max_value=10.0, step=0.01, value=3.0)
width = st.number_input("Width (mm)", min_value=100, max_value=10000, step=1, value=1220)
length = st.number_input("Length (mm)", min_value=100, max_value=10000, step=1, value=2440)
color = st.text_input("Color", "Solid & Metallic")
paint = st.text_input("Paint Type", "PE")

# Compute area
area_sqm = (width / 1000) * (length / 1000)

# Prepare input for prediction
input_df = pd.DataFrame([{
    "Country": country,
    "Product": product,
    "Alum_Thickness_mm": thickness,
    "Color": color,
    "Paint": paint,
    "Area_sqm": area_sqm
}])

# Predict price per sqm
pred_price_per_sqm = model.predict(input_df)[0]
total_price = pred_price_per_sqm * area_sqm

st.success(f"Predicted Ex-Works Price per Sqm: ${pred_price_per_sqm:.2f}")
st.success(f"Total Price for {area_sqm:.2f} sqm: ${total_price:.2f}")

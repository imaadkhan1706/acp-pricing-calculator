import streamlit as st
import pandas as pd

# Load the CSV
df = pd.read_csv("acp_pricing_table.csv")

st.title("ACP Pricing Calculator")

# Step 1: Select Country
country = st.selectbox("Select Country", sorted(df['Country'].unique()))
filtered_df = df[df['Country'] == country]

# Step 2: Select Alum Thickness
thickness = st.selectbox("Select Alum Thickness", sorted(filtered_df['Alum_Thickness'].unique()))
filtered_df = filtered_df[filtered_df['Alum_Thickness'] == thickness]

# Step 3: Select Width
width = st.selectbox("Select Width (mm)", sorted(filtered_df['Width_mm'].unique()))
filtered_df = filtered_df[filtered_df['Width_mm'] == width]

# Step 4: Select Length
length = st.selectbox("Select Length (mm)", sorted(filtered_df['Length_mm'].unique()))
filtered_df = filtered_df[filtered_df['Length_mm'] == length]

# Step 5: Select Color
color = st.selectbox("Select Color", sorted(filtered_df['Color'].unique()))
filtered_df = filtered_df[filtered_df['Color'] == color]

# Step 6: Select Paint
paint = st.selectbox("Select Paint", sorted(filtered_df['Paint'].unique()))
filtered_df = filtered_df[filtered_df['Paint'] == paint]

# Display price
if not filtered_df.empty:
    price = filtered_df['Exw_Price_USD'].values[0]
    st.success(f"Ex-Works Price per Sqm: ${price}")
else:
    st.warning("No matching configuration found.")

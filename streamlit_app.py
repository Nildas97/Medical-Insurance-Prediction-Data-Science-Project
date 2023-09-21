# importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# file location
model = pickle.load(open("model.pkl", "rb"))
encoder = pickle.load(open("target_encoder.pkl", "rb"))
transformer = pickle.load(open("transformer.pkl", "rb"))

# page title
st.title("Insurance Premium Prediction")

# features section
age = st.text_input("Enter Age", 18)
age = int(age)

gender = st.selectbox("Select gender", ("Male", "Female"))

bmi = st.text_input("Enter your BMI", 20)
bmi = float(bmi)

children = st.selectbox("Select No. of children", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
children = int(children)

smoker = st.selectbox("Select smoker category", ("Yes", "No"))

region = st.selectbox(
    "Select your region", ("southwest", "northeast", "northwest", "southeast")
)

# creating a dictionary to store all the above data
l = {}
l["age"] = age
l["sex"] = gender
l["bmi"] = bmi
l["children"] = children
l["smoker"] = smoker
l["region"] = region

# loading the data into a dataframe
df = pd.DataFrame(l, index=[0])

# encoding the categorical data into numerical
df["region"] = encoder.transform(df["region"])
df["sex"] = df["sex"].map({"male": 1, "female": 0})
df["smoker"] = df["smoker"].map({"yes": 1, "no": 0})

# prediction
df = transformer.transform(df)
y_pred = model.predict(df)

# results section
if st.button("Show Result"):
    st.header(f"{round(y_pred[0],2)} INR")


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load data
df = pd.read_csv("train.csv")

# Sidebar filter
st.sidebar.title("Filter Options")

classes = st.sidebar.multiselect(
    "Select Passenger Class",
    [1, 2, 3],
    default=[1, 2, 3]
)

df = df[df["Pclass"].isin(classes)]

# Title
st.title("Passengers & Survival Patterns")
st.write("Explore how gender, class and age affected survival.")

if df.empty:
    st.warning("Please select a passenger class.")
    st.stop()

# Key numbers
total = len(df)
survivors = df["Survived"].sum()
rate = survivors / total * 100

a, b, c = st.columns(3)

a.metric("Total Passengers", total)
b.metric("Total Survivors", survivors)
c.metric("Survival Rate", f"{rate:.1f}%")

st.divider()

# Chart 1: Gender
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Survival by Gender")

    gender = df.groupby(["Sex", "Survived"]).size().reset_index(name="Count")

    fig1 = px.bar(
        gender,
        x="Sex",
        y="Count",
        color="Survived",
        barmode="group",
        color_discrete_map={0: "tomato", 1: "mediumseagreen"}
    )

    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Passenger Class
with col2:
    st.subheader("Survival by Class")

    classes_data = df.groupby(["Pclass", "Survived"]).size().reset_index(name="Count")

    fig2 = px.bar(
        classes_data,
        x="Pclass",
        y="Count",
        color="Survived",
        barmode="stack",
        color_discrete_map={0: "tomato", 1: "mediumseagreen"}
    )

    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Age
with col3:
    st.subheader("Age Distribution")

    fig3 = px.histogram(
        df.dropna(subset=["Age"]),
        x="Age",
        color="Survived",
        color_discrete_map={0: "tomato", 1: "mediumseagreen"}
    )

    st.plotly_chart(fig3, use_container_width=True)

st.caption("Source: Kaggle Titanic Dataset")


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Titanic Survival Dashboard",
    layout="wide"
)

# Load dataset
df = pd.read_csv("train.csv")

# Sidebar filter
st.sidebar.title("Filter Options")

classes = st.sidebar.multiselect(
    "Select Passenger Class",
    [1, 2, 3],
    default=[1, 2, 3]
)

df = df[df["Pclass"].isin(classes)]

# Dashboard title
st.title("Passengers & Survival Patterns")
st.write("Explore how gender, class and age affected survival.")

# Check if data is available
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

# Survival labels
df["Survival Status"] = df["Survived"].map({
    0: "Died",
    1: "Survived"
})

# Chart 1 and Chart 2
col1, col2 = st.columns(2)

# Chart 1: Survival Rate by Gender
with col1:
    st.subheader("Survival Rate by Gender")

    gender_data = (
        df.groupby("Sex")["Survived"]
        .mean()
        .reset_index()
    )

    gender_data["Survival Rate"] = (
        gender_data["Survived"] * 100
    )

    fig1 = px.bar(
        gender_data,
        x="Survival Rate",
        y="Sex",
        orientation="h",
        text="Survival Rate",
        color="Sex",
        color_discrete_map={
            "female": "#B07CC6",
            "male": "#55A6D9"
        }
    )

    fig1.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig1.update_layout(
        xaxis_title="Survival Rate (%)",
        yaxis_title="Gender",
        showlegend=False,
        xaxis_range=[0, 100]
    )

    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Survival Rate by Class
with col2:
    st.subheader("Survival Rate by Class")

    class_data = (
        df.groupby("Pclass")["Survived"]
        .mean()
        .reset_index()
    )

    class_data["Survival Rate"] = (
        class_data["Survived"] * 100
    )

    fig2 = px.bar(
        class_data,
        x="Pclass",
        y="Survival Rate",
        text="Survival Rate",
        color="Survival Rate",
        color_continuous_scale="Purples"
    )

    fig2.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig2.update_layout(
        xaxis_title="Passenger Class",
        yaxis_title="Survival Rate (%)",
        coloraxis_showscale=False,
        yaxis_range=[0, 100]
    )

    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Age Distribution
st.subheader("Age Distribution by Survival")

fig3 = px.box(
    df.dropna(subset=["Age"]),
    x="Survival Status",
    y="Age",
    color="Survival Status",
    color_discrete_map={
        "Died": "#FF7058",
        "Survived": "#35B779"
    },
    points="outliers"
)

fig3.update_layout(
    xaxis_title="Survival Status",
    yaxis_title="Age",
    showlegend=False
)

st.plotly_chart(fig3, use_container_width=True)

# Data source
st.caption("Source: Kaggle Titanic Dataset")

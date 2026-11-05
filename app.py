
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Titanic Dashboard",
    page_icon="🚢",
    layout="wide"
)

# Load data
df = pd.read_csv("train.csv")

# Sidebar filter
st.sidebar.title("Filter Options")

classes = st.sidebar.multiselect(
    "Select Passenger Class",
    [1, 2, 3],
    default=[1, 2, 3],
    format_func=lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd'} Class"
)

data = df[df["Pclass"].isin(classes)]

# Dashboard title
st.title("🚢 Passengers & Survival Patterns")
st.caption("Explore how passenger class, gender and age affected survival.")

# Numbers
total = len(data)
survivors = int(data["Survived"].sum())
rate = survivors / total * 100 if total else 0

c1, c2, c3 = st.columns(3)

c1.metric("Total Passengers", total)
c2.metric("Total Survivors", survivors)
c3.metric("Survival Rate", f"{rate:.1f}%")

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Survival by Gender")

    gender = data.groupby(["Sex", "Survived"]).size().reset_index(name="Count")
    gender["Survival"] = gender["Survived"].map(
        {0: "Died", 1: "Survived"}
    )

    fig1 = px.bar(
        gender,
        x="Sex",
        y="Count",
        color="Survival",
        barmode="group",
        color_discrete_map={
            "Died": "#EF553B",
            "Survived": "#00CC96"
        }
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. Survival by Class")

    class_data = data.groupby(["Pclass", "Survived"]).size().reset_index(name="Count")
    class_data["Survival"] = class_data["Survived"].map(
        {0: "Died", 1: "Survived"}
    )
    class_data["Class"] = class_data["Pclass"].map({
        1: "First Class",
        2: "Second Class",
        3: "Third Class"
    })

    fig2 = px.bar(
        class_data,
        x="Class",
        y="Count",
        color="Survival",
        barmode="stack",
        color_discrete_map={
            "Died": "#EF553B",
            "Survived": "#00CC96"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. Age Distribution")

age_data = data.dropna(subset=["Age"])

fig3 = px.histogram(
    age_data,
    x="Age",
    color="Survived",
    nbins=20,
    color_discrete_map={
        0: "#EF553B",
        1: "#00CC96"
    },
    labels={"Survived": "Survival (0 = Died, 1 = Survived)"}
)

st.plotly_chart(fig3, use_container_width=True)

st.caption("Data source: Kaggle Titanic Dataset")

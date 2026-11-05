
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

if df.empty:
    st.warning("Please select at least one passenger class.")
    st.stop()

# Key numbers
total = len(df)
survivors = int(df["Survived"].sum())
died = total - survivors
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

colors = {
    "Died": "#FF6B5A",
    "Survived": "#35B779"
}

# First row
col1, col2 = st.columns(2)

# Chart 1: Overall Survival
with col1:
    st.subheader("Overall Survival")

    survival_data = pd.DataFrame({
        "Status": ["Survived", "Died"],
        "Passengers": [survivors, died]
    })

    fig1 = px.pie(
        survival_data,
        names="Status",
        values="Passengers",
        hole=0.55,
        color="Status",
        color_discrete_map=colors
    )

    fig1.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )

    fig1.update_layout(
        showlegend=False,
        margin=dict(t=30, b=20)
    )

    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Survival by Gender
with col2:
    st.subheader("Survival by Gender")

    gender_data = (
        df.groupby(["Sex", "Survival Status"])
        .size()
        .reset_index(name="Passengers")
    )

    fig2 = px.bar(
        gender_data,
        x="Sex",
        y="Passengers",
        color="Survival Status",
        barmode="group",
        text="Passengers",
        color_discrete_map=colors,
        category_orders={
            "Survival Status": ["Died", "Survived"]
        }
    )

    fig2.update_traces(
        textposition="outside"
    )

    fig2.update_layout(
        xaxis_title="Gender",
        yaxis_title="Number of Passengers",
        legend_title="Status",
        margin=dict(t=30, b=20)
    )

    st.plotly_chart(fig2, use_container_width=True)

# Second row
col3, col4 = st.columns(2)

# Chart 3: Survival by Class
with col3:
    st.subheader("Survival by Passenger Class")

    class_data = (
        df.groupby(["Pclass", "Survival Status"])
        .size()
        .reset_index(name="Passengers")
    )

    fig3 = px.bar(
        class_data,
        x="Pclass",
        y="Passengers",
        color="Survival Status",
        barmode="group",
        text="Passengers",
        color_discrete_map=colors,
        category_orders={
            "Survival Status": ["Died", "Survived"]
        }
    )

    fig3.update_traces(
        textposition="outside"
    )

    fig3.update_layout(
        xaxis_title="Passenger Class",
        yaxis_title="Number of Passengers",
        legend_title="Status",
        margin=dict(t=30, b=20)
    )

    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Age Distribution
with col4:
    st.subheader("Age Distribution")

    age_data = df.dropna(subset=["Age"])

    fig4 = px.histogram(
        age_data,
        x="Age",
        color="Survival Status",
        barmode="group",
        nbins=20,
        color_discrete_map=colors
    )

    fig4.update_layout(
        xaxis_title="Age",
        yaxis_title="Number of Passengers",
        legend_title="Status",
        margin=dict(t=30, b=20)
    )

    st.plotly_chart(fig4, use_container_width=True)

# Data source
st.caption("Source: Kaggle Titanic Dataset")

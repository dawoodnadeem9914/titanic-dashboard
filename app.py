
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Titanic Passenger Insights",
    layout="wide"
)

# Load dataset
df = pd.read_csv("train.csv")

# Prepare data
df["Port"] = df["Embarked"].map({
    "S": "Southampton",
    "C": "Cherbourg",
    "Q": "Queenstown"
}).fillna("Unknown")

df["Family Size"] = df["SibSp"] + df["Parch"] + 1

df["Family Group"] = df["Family Size"].apply(
    lambda x: "Alone" if x == 1
    else "Small Family" if x <= 4
    else "Large Family"
)

df["Status"] = df["Survived"].map({
    0: "Did Not Survive",
    1: "Survived"
})

# Sidebar filters
st.sidebar.title("Dashboard Filters")

selected_class = st.sidebar.multiselect(
    "Passenger Class",
    [1, 2, 3],
    default=[1, 2, 3]
)

df = df[df["Pclass"].isin(selected_class)]

if df.empty:
    st.warning("Please select at least one passenger class.")
    st.stop()

# Colours
colors = {
    "Did Not Survive": "#E76F51",
    "Survived": "#2A9D8F"
}

# Dashboard heading
st.title("Titanic Passenger Insights")

st.write(
    "Discover how passenger class, gender, "
    "boarding location and family size relate to survival."
)

# Summary numbers
total = len(df)
survivors = int(df["Survived"].sum())
deaths = total - survivors
survival_rate = survivors / total * 100

a, b, c, d = st.columns(4)

a.metric("Passengers", total)
b.metric("Survivors", survivors)
c.metric("Deaths", deaths)
d.metric("Survival Rate", f"{survival_rate:.1f}%")

st.divider()

# First row
col1, col2 = st.columns(2)

# Chart 1: Survival Rate by Class
with col1:
    st.subheader("Survival Rate by Class")

    class_data = (
        df.groupby("Pclass")["Survived"]
        .mean()
        .reset_index()
    )

    class_data["Survival Rate"] = (
        class_data["Survived"] * 100
    )

    class_data["Class"] = class_data["Pclass"].map({
        1: "First Class",
        2: "Second Class",
        3: "Third Class"
    })

    fig1 = px.bar(
        class_data,
        x="Survival Rate",
        y="Class",
        orientation="h",
        text="Survival Rate",
        color="Class",
        color_discrete_sequence=[
            "#264653",
            "#2A9D8F",
            "#E9C46A"
        ]
    )

    fig1.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig1.update_layout(
        xaxis_title="Survival Rate (%)",
        yaxis_title="Passenger Class",
        showlegend=False,
        height=340,
        margin=dict(t=35, b=40)
    )

    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Survival by Gender
with col2:
    st.subheader("Survival by Gender")

    gender_data = (
        df.groupby(["Sex", "Status"])
        .size()
        .reset_index(name="Passengers")
    )

    gender_data["Percentage"] = (
        gender_data.groupby("Sex")["Passengers"]
        .transform(lambda x: x / x.sum() * 100)
    )

    fig2 = px.bar(
        gender_data,
        x="Sex",
        y="Percentage",
        color="Status",
        text=gender_data["Percentage"].round(1).astype(str) + "%",
        barmode="stack",
        color_discrete_map=colors
    )

    fig2.update_layout(
        xaxis_title="Gender",
        yaxis_title="Percentage of Passengers (%)",
        yaxis_range=[0, 100],
        height=340,
        legend_title="Outcome",
        margin=dict(t=35, b=40)
    )

    st.plotly_chart(fig2, use_container_width=True)

# Second row
col3, col4 = st.columns(2)

# Chart 3: Passengers by Boarding Port
with col3:
    st.subheader("Passengers by Boarding Port")

    port_data = (
        df.groupby("Port")
        .size()
        .reset_index(name="Passengers")
        .sort_values("Passengers")
    )

    fig3 = px.bar(
        port_data,
        x="Passengers",
        y="Port",
        orientation="h",
        text="Passengers",
        color="Port",
        color_discrete_sequence=[
            "#457B9D",
            "#A8DADC",
            "#1D3557",
            "#F4A261"
        ]
    )

    fig3.update_layout(
        xaxis_title="Number of Passengers",
        yaxis_title="Boarding Port",
        showlegend=False,
        height=340,
        margin=dict(t=35, b=40)
    )

    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Survival by Family Size
with col4:
    st.subheader("Survival by Family Size")

    family_data = (
        df.groupby(["Family Group", "Status"])
        .size()
        .reset_index(name="Passengers")
    )

    fig4 = px.bar(
        family_data,
        x="Family Group",
        y="Passengers",
        color="Status",
        barmode="group",
        text="Passengers",
        color_discrete_map=colors,
        category_orders={
            "Family Group": [
                "Alone",
                "Small Family",
                "Large Family"
            ]
        }
    )

    fig4.update_layout(
        xaxis_title="Family Group",
        yaxis_title="Number of Passengers",
        height=340,
        legend_title="Outcome",
        margin=dict(t=35, b=40)
    )

    st.plotly_chart(fig4, use_container_width=True)

# Data source
st.caption("Dataset Source: Kaggle Titanic Dataset")

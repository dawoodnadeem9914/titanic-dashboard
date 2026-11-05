
import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Titanic Data Explorer",
    page_icon="🚢",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}
h1 {
    color: #183B56;
}
h2, h3 {
    color: #245B75;
}
[data-testid="stMetric"] {
    background: #F0F6FA;
    padding: 18px;
    border-radius: 12px;
    border-left: 4px solid #249E9A;
}
</style>
""", unsafe_allow_html=True)

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

# Sidebar
st.sidebar.title("Dashboard Filters")

selected_class = st.sidebar.multiselect(
    "Select Passenger Class",
    [1, 2, 3],
    default=[1, 2, 3]
)

df = df[df["Pclass"].isin(selected_class)]

if df.empty:
    st.warning("Please select at least one class.")
    st.stop()

# Colours
colors = {
    "Did Not Survive": "#E76F51",
    "Survived": "#249E9A"
}

# Common chart layout
def chart_style(fig):
    fig.update_layout(
        template="plotly_white",
        height=350,
        font=dict(
            family="Arial",
            size=13,
            color="#29465B"
        ),
        margin=dict(l=45, r=35, t=35, b=45),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        gridcolor="#E5EDF2",
        zeroline=False
    )
    return fig

# Dashboard title
st.title("Titanic Data Explorer")
st.write(
    "An overview of passenger survival, "
    "gender, class, boarding location and family size."
)

st.divider()

# Key metrics
total = len(df)
survivors = int(df["Survived"].sum())
deaths = total - survivors
rate = survivors / total * 100

a, b, c, d = st.columns(4)

a.metric("Total Passengers", f"{total:,}")
b.metric("Survivors", f"{survivors:,}")
c.metric("Deaths", f"{deaths:,}")
d.metric("Survival Rate", f"{rate:.1f}%")

st.divider()

# First row
col1, col2 = st.columns(2, gap="large")

# Chart 1: Survival by Class
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

    class_data["Passenger Class"] = (
        class_data["Pclass"].map({
            1: "First Class",
            2: "Second Class",
            3: "Third Class"
        })
    )

    fig1 = px.bar(
        class_data,
        x="Passenger Class",
        y="Survival Rate",
        text="Survival Rate",
        color="Passenger Class",
        color_discrete_map={
            "First Class": "#245B75",
            "Second Class": "#249E9A",
            "Third Class": "#76B7B2"
        }
    )

    fig1.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig1.update_layout(
        showlegend=False,
        yaxis_title="Survival Rate (%)",
        xaxis_title="Passenger Class",
        yaxis_range=[0, 80]
    )

    chart_style(fig1)
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Survival by Gender
with col2:
    st.subheader("Survival by Gender")

    gender_data = (
        df.groupby(["Sex", "Status"])
        .size()
        .reset_index(name="Passengers")
    )

    fig2 = px.bar(
        gender_data,
        x="Sex",
        y="Passengers",
        color="Status",
        barmode="group",
        text="Passengers",
        color_discrete_map=colors,
        category_orders={
            "Status": ["Survived", "Did Not Survive"]
        }
    )

    fig2.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig2.update_layout(
        xaxis_title="Gender",
        yaxis_title="Number of Passengers"
    )

    chart_style(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# Second row
col3, col4 = st.columns(2, gap="large")

# Chart 3: Boarding Port
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
            "#183B56",
            "#249E9A",
            "#76B7B2",
            "#E9C46A"
        ]
    )

    fig3.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig3.update_layout(
        xaxis_title="Number of Passengers",
        yaxis_title="Boarding Port",
        showlegend=False
    )

    chart_style(fig3)
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
            ],
            "Status": [
                "Survived",
                "Did Not Survive"
            ]
        }
    )

    fig4.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig4.update_layout(
        xaxis_title="Family Group",
        yaxis_title="Number of Passengers"
    )

    chart_style(fig4)
    st.plotly_chart(fig4, use_container_width=True)

# Footer
st.divider()
st.caption("Data Source: Kaggle Titanic Dataset")

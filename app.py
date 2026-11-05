
# Chart colours and labels
df["Survival Status"] = df["Survived"].map({
    0: "Died",
    1: "Survived"
})

colors = {
    "Died": "tomato",
    "Survived": "mediumseagreen"
}

col1, col2, col3 = st.columns(3)

# Chart 1: Gender
with col1:
    st.subheader("Survival by Gender")

    gender = df.groupby(
        ["Sex", "Survival Status"]
    ).size().reset_index(name="Count")

    fig1 = px.bar(
        gender,
        x="Sex",
        y="Count",
        color="Survival Status",
        barmode="group",
        color_discrete_map=colors
    )

    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Passenger Class
with col2:
    st.subheader("Survival by Class")

    class_data = df.groupby(
        ["Pclass", "Survival Status"]
    ).size().reset_index(name="Count")

    fig2 = px.bar(
        class_data,
        x="Pclass",
        y="Count",
        color="Survival Status",
        barmode="stack",
        color_discrete_map=colors
    )

    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Age
with col3:
    st.subheader("Age Distribution")

    fig3 = px.histogram(
        df.dropna(subset=["Age"]),
        x="Age",
        color="Survival Status",
        color_discrete_map=colors
    )

    st.plotly_chart(fig3, use_container_width=True)

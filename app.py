import streamlit as st
import pandas as pd
import altair as alt

st.title("CO₂ Emissions — Best and Worst Countries")

st.write(
    "Upload your CO₂ summary dataset to view the highest and lowest emitting countries."
)

uploaded_file = st.file_uploader("Upload Summary CSV", type=["csv"])

if uploaded_file is not None:
    # Load dataset
    T = pd.read_csv(uploaded_file)

    # Validate required columns
    if "Country" not in T.columns or "Sum" not in T.columns:
        st.error("Dataset must contain 'Country' and 'Sum' columns.")
    else:
        # Slider for number of countries to show
        num = st.slider("Number of countries to display", 5, 30, 10)

        # Choose best or worst countries
        choice = st.radio(
            "Select view:",
            ("Best (Lowest CO₂ Emitters)", "Worst (Highest CO₂ Emitters)")
        )

        # Compute subset
        if choice == "Best (Lowest CO₂ Emitters)":
            subset = T.nsmallest(num, "Sum")
            title = f"Top {num} Countries With Lowest Total CO₂ Emissions"
        else:
            subset = T.nlargest(num, "Sum")
            title = f"Top {num} Countries With Highest Total CO₂ Emissions"

        # Create Altair bar chart
        chart = (
            alt.Chart(subset)
            .mark_bar()
            .encode(
                x=alt.X("Country:N", sort=None, title="Country"),
                y=alt.Y("Sum:Q", title="Total Emissions (Sum)"),
                tooltip=["Country", "Sum"]
            )
            .properties(
                width=700,
                height=400,
                title=title
            )
        )

        # Display chart
        st.altair_chart(chart, use_container_width=True)

else:
    st.info("Please upload your summary dataset to generate graphs.")

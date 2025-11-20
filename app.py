import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("CO₂ Emissions — Best and Worst Countries")

st.write(
    "Upload your CO₂ summary dataset to view the highest and lowest emitting countries."
)

uploaded_file = st.file_uploader("Upload Summary CSV", type=["csv"])

if uploaded_file is not None:
    # Load dataset
    T = pd.read_csv(uploaded_file)

    # Keep only needed columns
    if "Country" not in T.columns or "Sum" not in T.columns:
        st.error("Dataset must contain 'Country' and 'Sum' columns.")
    else:
        # User selects number of countries to display
        num = st.slider("Number of countries to display", 5, 30, 10)

        # Choose best or worst countries
        choice = st.radio(
            "Select view:",
            ("Best (Lowest CO₂ Emitters)", "Worst (Highest CO₂ Emitters)")
        )

        # Compute best or worst
        if choice == "Best (Lowest CO₂ Emitters)":
            subset = T.nsmallest(num, "Sum")
            title = f"Top {num} Countries With Lowest Total CO₂ Emissions"
        else:
            subset = T.nlargest(num, "Sum")
            title = f"Top {num} Countries With Highest Total CO₂ Emissions"

        # Plot graph
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(subset["Country"], subset["Sum"], color="skyblue")
        ax.set_xticklabels(subset["Country"], rotation=45, ha="right")
        ax.set_ylabel("Total Emissions (Sum)")
        ax.set_title(title)

        st.pyplot(fig)

else:
    st.info("Please upload your summary dataset to generate graphs.")

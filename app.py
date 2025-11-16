import streamlit as st
import pandas as pd

st.title("CO₂ Emissions Summary by Country")

st.write(
    "Upload a CSV file with at least two columns: "
    "`Country` and `CO2Emission_Tons_`."
)

uploaded_file = st.file_uploader("Upload CO₂ CSV", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    T = pd.read_csv(uploaded_file)

    # Drop missing rows
    T = T.dropna()

    # Column names
    countryVar = "Country"
    emissionVar = "CO2Emission_Tons_"

    # Check columns exist
    if countryVar not in T.columns or emissionVar not in T.columns:
        st.error(f"CSV must contain '{countryVar}' and '{emissionVar}' columns.")
    else:
        # Group by country and compute stats
        grouped = T.groupby(countryVar)[emissionVar]

        Result = grouped.agg(
            Count="count",
            Mean="mean",
            Std="std",
            Min="min",
            Median="median",
            Max="max",
            Sum="sum"
        ).reset_index()

        st.subheader("Summary Statistics")
        st.dataframe(Result)
else:
    st.info("Upload a CSV file to see the summary statistics.")

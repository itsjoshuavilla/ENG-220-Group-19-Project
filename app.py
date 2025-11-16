import streamlit as st
import pandas as pd

st.title("CO₂ Emissions Summary by Country")

st.write(
    "Upload the *summary* CSV file with these columns: "
    "`Country`, `Count`, `Mean`, `Std`, `Min`, `Median`, `Max`, `Sum`."
)

uploaded_file = st.file_uploader("Upload CO₂ Summary CSV", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    T = pd.read_csv(uploaded_file)

    # Drop missing rows (optional)
    T = T.dropna()

    required_cols = ["Country", "Count", "Mean", "Std", "Min", "Median", "Max", "Sum"]
    missing = [c for c in required_cols if c not in T.columns]

    if missing:
        st.error(f"CSV is missing these columns: {', '.join(missing)}")
    else:
        st.subheader("Summary Statistics (from file)")
        st.dataframe(T)
else:
    st.info("Upload your summary CSV to see the table.")

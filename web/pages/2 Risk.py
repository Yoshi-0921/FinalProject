import streamlit as st
import pandas as pd
import datetime
import numpy as np
from forex_python.converter import CurrencyRates, CurrencyCodes
from Home import bucket_df, income_df, transaction_df

# Initial Currency Settings
c = CurrencyRates()
ccode = CurrencyCodes()
if "currency" not in st.session_state:
    st.session_state["currency"] = "JPY"
if __name__ == "__main__":
    st.set_page_config(page_title="Plotting Demo", page_icon="📈")
    st.session_state["currency"] = (
        "JPY" if "currency" not in st.session_state else st.session_state["currency"]
    )

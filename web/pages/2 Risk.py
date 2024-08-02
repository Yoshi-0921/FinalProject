import datetime

import numpy as np
import pandas as pd
import streamlit as st
from forex_python.converter import CurrencyCodes, CurrencyRates
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

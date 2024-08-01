import streamlit as st
from forex_python.converter import CurrencyRates, CurrencyCodes
import pandas as pd

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.write("# Hey! 👋")


if "currency" not in st.session_state:
    st.session_state["currency"] = "JPY"


ccode = CurrencyCodes()

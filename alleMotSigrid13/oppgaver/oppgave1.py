import streamlit as st

def oppgave():
    title = st.markdown("**oppgave 1**", unsafe_allow_html=True)
    txt = st.markdown("dette er en tekst som skal være under oppgaven")
    slider = st.slider("Velg et tall", 0, 100)
    return title, txt, slider

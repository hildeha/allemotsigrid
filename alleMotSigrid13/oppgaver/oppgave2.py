import streamlit as st

def oppgave():
    title = st.markdown("**oppgave 2**", unsafe_allow_html=True)
    txt = st.markdown("dette er en NY tekst ")
    slider = st.slider("Velg et tall", 0, 4)
    return title, txt, slider
import streamlit as st
from views.tab_estimation import render_tab_estimation
from views.tab_tournois import render_tab_tournois
from views.tab_comparaison import render_tab_comparaison

st.set_page_config(page_title="Padel • Estimation & Scénarios", page_icon="🎾", layout="wide")
st.title("🎾 Padel — Estimation des recettes & comparaison de formules")
st.caption("Hypothèses par défaut modifiables. 2 pistes, créneaux de 1h30, 365 jours/an.")

TABS = [
    ("Estimateur recettes", render_tab_estimation),
    ("Tournois", render_tab_tournois),
    ("Comparaison des formules", render_tab_comparaison),
]

labels = [t[0] for t in TABS]
views = [t[1] for t in TABS]

selected = st.tabs(labels)
for tab, view in zip(selected, views):
    with tab:
        view()
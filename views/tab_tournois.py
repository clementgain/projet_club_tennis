import streamlit as st
from models.calculs import TournoiParams, calc_tournois, euros

def render_tab_tournois():
    st.subheader("Tournois — simulation détaillée")
    st.caption("Paramétrez chaque format, visualisez recette brute, dépenses, bénéfice net et agrégat annuel.")

    col1, col2, col3 = st.columns(3)
    with col1:
        n_soirees = st.number_input("Soirées / an", 0, 100, 6, key="tour_n_soirees")
        prix_soiree = st.slider("Prix joueur — Soirée", 20.0, 25.0, 22.5, 0.5, key="tour_prix_soiree")
        eq_s = st.number_input("Équipes — Soirée", 2, 64, 8, key="tour_eq_s")
        duree_s = st.slider("Durée Soirée (j)", 0.25, 1.0, 0.5, 0.25, key="tour_duree_s", help="Pour l'estimation du cout du JA")
    with col2:
        n_journees = st.number_input("Journées / an", 0, 100, 6, key="tour_n_journees")
        prix_journee = st.slider("Prix joueur — Journée", 20.0, 25.0, 22.5, 0.5, key="tour_prix_journee")
        eq_j = st.number_input("Équipes — Journée", 2, 64, 12, key="tour_eq_j")
        duree_j = st.slider("Durée Journée (j)", 0.5, 2.0, 1.0, 0.5, key="tour_duree_j", help="Pour l'estimation du cout du JA")
    with col3:
        n_deux = st.number_input("Tournois 2 jours / an", 0, 100, 0, key="tour_n_deux")
        prix_deux = st.slider("Prix joueur — 2 jours", 20.0, 25.0, 22.5, 0.5, key="tour_prix_deux")
        eq_2 = st.number_input("Équipes — 2 jours", 2, 64, 20, key="tour_eq_2")
        duree_2 = st.slider("Durée 2 jours (j)", 1.0, 3.0, 2.0, 0.5, key="tour_duree_2", help="Pour l'estimation du cout du JA")

    st.markdown("---")
    colx, coly, colz = st.columns(3)
    with colx:
        ja = st.number_input("Juge-arbitre (€/jour)", 0.0, 500.0, 50.0, 5.0, key="tour_ja")
        droits = st.number_input("Droits (€/tournoi)", 0.0, 500.0, 40.0, 5.0, key="tour_droits")
    with coly:
        tubes_j = st.number_input("Tubes/jour", 0, 100, 16, 1, key="tour_tubes")
        prix_tube = st.number_input("Prix/tube (€)", 0.0, 50.0, 5.0, 0.5, key="tour_prix_tube")
    with colz:
        benef_bar = st.number_input("Bénéfice bar (€/jour)", 0.0, 1000.0, 150.0, 10.0, key="tour_benef_bar")
        autre_recette = st.number_input("Autre recette (€/jour)", 0.0, 1000.0, 0.0, 10.0, key="tour_autre_recette")

    params = TournoiParams(
        n_soirees=n_soirees, n_journees=n_journees, n_deux_jours=n_deux,
        prix_joueur_soiree=prix_soiree, prix_joueur_journee=prix_journee, prix_joueur_deux_jours=prix_deux,
        equipes_soiree=eq_s, equipes_journee=eq_j, equipes_deux_jours=eq_2,
        duree_soiree=duree_s, duree_journee=duree_j, duree_deux_jours=duree_2,
        ja_cout_par_jour=ja, droit_enregistrement=droits,
        balles_tubes_par_jour=tubes_j, balles_prix_par_tube=prix_tube,
        benef_bar_par_jour=benef_bar, autre_recette_par_jour=autre_recette,
    )

    out = calc_tournois(params)
    unit = out["unitaire"]
    ann = out["annuel"]

    st.markdown("### Unitaire")
    c1, c2, c3 = st.columns(3)
    for i, (label, d) in enumerate([
        ("Soirée", unit["soiree"]),
        ("Journée", unit["journee"]),
        ("2 jours", unit["deux_jours"]),
    ]):
        with (c1 if i == 0 else c2 if i == 1 else c3):
            st.metric(f"{label} — Recette brute", euros(d["recette_brute"]))
            st.metric(f"{label} — Dépenses", euros(d["depenses"]))
            st.metric(f"{label} — Recettes annexes", euros(d["recettes_annexes"]))
            st.metric(f"{label} — Bénéfice net", euros(d["benefice_net"]))

    st.markdown("### Annuel")
    cc1, cc2, cc3, cc4 = st.columns(4)
    with cc1: st.metric("Recette brute", euros(ann["recette_brute"]))
    with cc2: st.metric("Dépenses", euros(ann["depenses"]))
    with cc3: st.metric("Recettes annexes", euros(ann["recettes_annexes"]))
    with cc4: st.metric("Bénéfice net", euros(ann["benefice_net"]))

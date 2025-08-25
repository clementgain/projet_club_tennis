import streamlit as st
import pandas as pd
import altair as alt
from models.calculs import (
    calc_tournois, TournoiParams,
    ScenarioAdhesionIllimitee, ScenarioLocationPourTous,
    calc_scenario_adhesion, calc_scenario_location,
    capacity_reservations_per_day, euros
)

def render_tab_comparaison():
    st.subheader("Comparaison des formules — Adhésion illimitée vs Location horaire")

    st.markdown("#### Hypothèse de capacité")
    colcap1, colcap2 = st.columns(2)
    with colcap1:
        open_hours = st.slider("Heures d'ouverture par jour", 6.0, 18.0, 12.0, 0.5, key="comp_open_hours")
    with colcap2:
        courts = st.number_input("Nombre de pistes", 1, 8, 2, key="comp_courts")
    cap = capacity_reservations_per_day(open_hours, courts)
    st.caption(f"Capacité théorique = **{cap} créneaux de 1h30/jour** (toutes pistes).")

    st.markdown("---")
    st.markdown("### Paramètres des deux formules")

    cola, colb = st.columns(2)
    with cola:
        st.markdown("**Formule A — Adhésion illimitée**")
        prix_adh_unique = st.number_input("Prix adhésion (€/an)", 0.0, 1000.0, 140.0, 5.0, key="comp_prix_adh")
        nb_adh = st.number_input("Nombre d'adhérents", 0, 5000, 200, 10, key="comp_nb_adh")
        prix_nonadh = st.number_input("Prix non-adhérent (€/joueur)", 0.0, 50.0, 7.0, 0.5, key="comp_prix_nonadh")
        nb_resa_A = st.slider("Réservations/jour (Formule A)", 0, cap, min(cap, 4), key="comp_nb_resa_A")
        prop_adh_A = st.slider("Proportion d'adhérents dans les réservations", 0.0, 1.0, 0.6, 0.05, key="comp_prop_adh")

    with colb:
        st.markdown("**Formule B — Location horaire pour tous**")
        prix_loc = st.number_input("Prix (€/joueur)", 0.0, 50.0, 7.0, 0.5, key="comp_prix_loc")
        nb_resa_B = st.slider("Réservations/jour (Formule B)", 0, cap, min(cap, 4), key="comp_nb_resa_B")

    st.markdown("---")
    st.markdown("### Tournois (communs aux deux formules)")

    col1, col2, col3 = st.columns(3)
    with col1:
        n_soirees = st.number_input("Soirées / an", 0, 100, 6, key="comp_n_soirees")
        prix_soiree = st.slider("Prix joueur — Soirée", 20.0, 25.0, 22.5, 0.5, key="comp_prix_soiree")
    with col2:
        n_journees = st.number_input("Journées / an", 0, 100, 6, key="comp_n_journees")
        prix_journee = st.slider("Prix joueur — Journée", 20.0, 25.0, 22.5, 0.5, key="comp_prix_journee")
    with col3:
        n_deux = st.number_input("2 jours / an", 0, 100, 0, key="comp_n_deux")
        prix_deux = st.slider("Prix joueur — 2 jours", 20.0, 25.0, 22.5, 0.5, key="comp_prix_deux")

    colx, coly, colz = st.columns(3)
    with colx:
        ja = st.number_input("Juge-arbitre (€/jour)", 0.0, 500.0, 50.0, 5.0, key="comp_ja")
        droits = st.number_input("Droits (€/tournoi)", 0.0, 500.0, 40.0, 5.0, key="comp_droits")
    with coly:
        tubes_j = st.number_input("Tubes/jour", 0, 100, 16, 1, key="comp_tubes")
        prix_tube = st.number_input("Prix/tube (€)", 0.0, 50.0, 5.0, 0.5, key="comp_prix_tube")
    with colz:
        benef_bar = st.number_input("Bénéfice bar (€/jour)", 0.0, 1000.0, 150.0, 10.0, key="comp_benef_bar")
        autre_recette = st.number_input("Autre recette (€/jour)", 0.0, 1000.0, 0.0, 10.0, key="comp_autre_recette")

    params_t = TournoiParams(
        n_soirees=n_soirees, n_journees=n_journees, n_deux_jours=n_deux,
        prix_joueur_soiree=prix_soiree, prix_joueur_journee=prix_journee, prix_joueur_deux_jours=prix_deux,
        ja_cout_par_jour=ja, droit_enregistrement=droits,
        balles_tubes_par_jour=tubes_j, balles_prix_par_tube=prix_tube,
        benef_bar_par_jour=benef_bar, autre_recette_par_jour=autre_recette,
    )

    benef_tournois = calc_tournois(params_t)["annuel"]["benefice_net"]

    # Calculs formulaires
    sA = ScenarioAdhesionIllimitee(
        prix_adhesion_unique=prix_adh_unique,
        nb_adherents=nb_adh,
        prix_non_adh_resa=prix_nonadh,
        nb_resa_jour=nb_resa_A,
        proportion_adh_resa=prop_adh_A,
    )
    sB = ScenarioLocationPourTous(
        prix_resa_joueur=prix_loc,
        nb_resa_jour=nb_resa_B,
    )

    outA = calc_scenario_adhesion(sA)
    outB = calc_scenario_location(sB)

    totalA = outA["total_hors_tournois"] + benef_tournois
    totalB = outB["total_hors_tournois"] + benef_tournois

    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### Formule A — Détails")
        st.metric("Adhésions", euros(outA["recettes_adhesions"]))
        st.metric("Réservations (non-adh)", euros(outA["recettes_reservations"]))
        st.metric("Bénéfice net tournois", euros(benef_tournois))
        st.metric("Total annuel (net)", euros(totalA))
    with colB:
        st.markdown("#### Formule B — Détails")
        st.metric("Adhésions", "—")
        st.metric("Réservations", euros(outB["recettes_reservations"]))
        st.metric("Bénéfice net tournois", euros(benef_tournois))
        st.metric("Total annuel (net)", euros(totalB))

    st.markdown("---")
    st.markdown("### Graphiques")

    # Barres empilées : composition
    df_comp = pd.DataFrame([
        {"Formule": "Adhésion illimitée", "Poste": "Adhésions", "Montant": outA["recettes_adhesions"]},
        {"Formule": "Adhésion illimitée", "Poste": "Réservations", "Montant": outA["recettes_reservations"]},
        {"Formule": "Adhésion illimitée", "Poste": "Tournois (net)", "Montant": benef_tournois},
        {"Formule": "Location horaire", "Poste": "Adhésions", "Montant": 0.0},
        {"Formule": "Location horaire", "Poste": "Réservations", "Montant": outB["recettes_reservations"]},
        {"Formule": "Location horaire", "Poste": "Tournois (net)", "Montant": benef_tournois},
    ])

    chart_comp = (
        alt.Chart(df_comp)
        .mark_bar()
        .encode(
            x=alt.X("Formule:N", title="Formule"),
            y=alt.Y("sum(Montant):Q", title="Montant annuel (€)"),
            color=alt.Color("Poste:N"),
            tooltip=["Formule", "Poste", alt.Tooltip("Montant:Q", format=",.0f")],
        )
    )
    st.altair_chart(chart_comp, use_container_width=True)

    # Sensibilité aux réservations/jour
    x_vals = list(range(0, cap + 1))
    df_sens = pd.DataFrame({
        "Resa/jour": x_vals,
        "Adhésion illimitée": [
            calc_scenario_adhesion(ScenarioAdhesionIllimitee(
                prix_adhesion_unique=prix_adh_unique,
                nb_adherents=nb_adh,
                prix_non_adh_resa=prix_nonadh,
                nb_resa_jour=x,
                proportion_adh_resa=prop_adh_A,
            ))["total_hors_tournois"] + benef_tournois for x in x_vals
        ],
        "Location horaire": [
            calc_scenario_location(ScenarioLocationPourTous(
                prix_resa_joueur=prix_loc,
                nb_resa_jour=x,
            ))["total_hors_tournois"] + benef_tournois for x in x_vals
        ],
    })

    df_melt = df_sens.melt("Resa/jour", var_name="Formule", value_name="Total annuel (€)")
    chart_sens = (
        alt.Chart(df_melt)
        .mark_line(point=True)
        .encode(
            x=alt.X("Resa/jour:Q", title="Réservations par jour"),
            y=alt.Y("Total annuel (€):Q", title="Total annuel (€)"),
            color="Formule:N",
            tooltip=["Formule", "Resa/jour", alt.Tooltip("Total annuel (€):Q", format=",.0f")],
        )
    )
    st.altair_chart(chart_sens, use_container_width=True)

    # Sensibilité proportion d'adhérents (Formule A)
    props = [x / 100 for x in range(0, 101, 5)]
    df_prop = pd.DataFrame({
        "Proportion adhérents": props,
        "Total annuel (€)": [
            calc_scenario_adhesion(ScenarioAdhesionIllimitee(
                prix_adhesion_unique=prix_adh_unique,
                nb_adherents=nb_adh,
                prix_non_adh_resa=prix_nonadh,
                nb_resa_jour=nb_resa_A,
                proportion_adh_resa=p,
            ))["total_hors_tournois"] + benef_tournois for p in props
        ]
    })

    chart_prop = (
        alt.Chart(df_prop)
        .mark_line(point=True)
        .encode(
            x=alt.X("Proportion adhérents:Q", title="Proportion d'adhérents dans les réservations"),
            y=alt.Y("Total annuel (€):Q", title="Total annuel (€)"),
            tooltip=[alt.Tooltip("Proportion adhérents:Q", format=".0%"), alt.Tooltip("Total annuel (€):Q", format=",.0f")],
        )
    )
    st.altair_chart(chart_prop, use_container_width=True)

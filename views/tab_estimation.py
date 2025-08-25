import streamlit as st
from models.calculs import (
    BaseInputs, TournoiParams, calc_recettes_base, calc_tournois, euros,
    JOUEURS_PAR_PISTE, JOURS_PAR_AN
)

def render_tab_estimation():
    st.subheader("Estimateur recettes — Adhésions & Réservations")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Adhésions**")
        prix_adh_tennis = st.number_input("Prix adhésion Padel si déjà adhérent Tennis (€)", min_value=0.0, value=50.0, step=5.0)
        nb_adh_tennis = st.number_input("Nombre adhérents Padel déjà adhérents Tennis", min_value=0, value=40, step=1)
        prix_adh_seul = st.number_input("Prix adhésion Padel seul (€)", min_value=0.0, value=120.0, step=5.0)
        nb_adh_seul = st.number_input("Nombre d'adhérents Padel seul", min_value=0, value=30, step=1)

    with col2:
        st.markdown("**Réservations** (1h30, 4 joueurs/piste)")
        prix_resa_adh = st.number_input("Prix réservation — adhérent (€/joueur)", min_value=0.0, value=6.0, step=1.0)
        prix_resa_nonadh = st.number_input("Prix réservation — non adhérent (€/joueur)", min_value=0.0, value=10.0, step=1.0)
        nb_pistes_par_jour = st.slider("Nombre moyen de pistes réservées / jour (toutes pistes)", 0.0, 48.0, 10.0, 0.5)
        prop_adh_resa = st.slider("Proportion d'adhérents dans les réservations", 0.0, 1.0, 0.6, 0.05)

    inp = BaseInputs(
        prix_adh_tennis, nb_adh_tennis, prix_adh_seul, nb_adh_seul,
        prix_resa_adh, prix_resa_nonadh, nb_pistes_par_jour, prop_adh_resa
    )

    base = calc_recettes_base(inp)

    st.divider()
    st.markdown("### Tournois — paramètres")

    with st.expander("Réglages tournois"):
        use_unique_price = st.checkbox("Utiliser un prix unique par joueur pour tous les formats", value=True, key="est_use_unique_price")
        if use_unique_price:
            unique_price = st.slider("Prix joueur (tous formats)", 20.0, 25.0, 22.5, 0.5, key="est_unique_price")
            prix_soiree = prix_journee = prix_deux = unique_price
        else:
            colp1, colp2, colp3 = st.columns(3)
            with colp1:
                prix_soiree = st.slider("Prix joueur — Soirée", 20.0, 25.0, 22.5, 0.5, key="est_prix_soiree")
            with colp2:
                prix_journee = st.slider("Prix joueur — Journée", 20.0, 25.0, 22.5, 0.5, key="est_prix_journee")
            with colp3:
                prix_deux = st.slider("Prix joueur — 2 jours", 20.0, 25.0, 22.5, 0.5, key="est_prix_deux")

        cols_f, colx, coly = st.columns([2,1,1])
        with cols_f:
            st.markdown("**Fréquence annuelle**")
            n_soirees = st.number_input("Tournois Soirée / an", 0, 100, 6, 1, key="est_n_soirees")
            n_journees = st.number_input("Tournois Journée / an", 0, 100, 6, 1, key="est_n_journees")
            n_deux = st.number_input("Tournois 2 jours / an", 0, 100, 0, 1, key="est_n_deux")
        with colx:
            st.markdown("**Dépenses**")
            ja = st.number_input("Juge-arbitre (€/jour)", 0.0, 500.0, 50.0, 5.0, key="est_ja")
            droits = st.number_input("Droits enregistrement (€/tournoi)", 0.0, 500.0, 40.0, 5.0, key="est_droits")
        with coly:
            st.markdown("**Balles**")
            tubes_j = st.number_input("Tubes/jour", 0, 100, 16, 1, key="est_tubes")
            prix_tube = st.number_input("Prix/tube (€/3 balles)", 0.0, 50.0, 5.0, 0.5, key="est_prix_tube")

        colb1, colb2 = st.columns(2)
        with colb1:
            benef_bar = st.number_input("Bénéfice bar (€/jour)", 0.0, 1000.0, 150.0, 10.0, key="est_benef_bar")
        with colb2:
            autre_recette = st.number_input("Autre recette (€/jour)", 0.0, 1000.0, 0.0, 10.0, key="est_autre_recette")

        st.markdown("**Durées & capacités par format**")
        duree_s = st.slider("Durée Soirée (jours)", 0.25, 1.0, 0.5, 0.25, key="est_duree_s")
        duree_j = st.slider("Durée Journée (jours)", 0.5, 2.0, 1.0, 0.5, key="est_duree_j")
        duree_2 = st.slider("Durée 2 jours (jours)", 1.0, 3.0, 2.0, 0.5, key="est_duree_2")
        eq_s = st.number_input("Équipes — Soirée", 2, 64, 8, 1, key="est_eq_s")
        eq_j = st.number_input("Équipes — Journée", 2, 64, 12, 1, key="est_eq_j")
        eq_2 = st.number_input("Équipes — 2 jours", 2, 64, 20, 1, key="est_eq_2")

    tparams = TournoiParams(
        n_soirees=n_soirees, n_journees=n_journees, n_deux_jours=n_deux,
        prix_joueur_soiree=prix_soiree, prix_joueur_journee=prix_journee, prix_joueur_deux_jours=prix_deux,
        ja_cout_par_jour=ja, droit_enregistrement=droits,
        balles_tubes_par_jour=tubes_j, balles_prix_par_tube=prix_tube,
        benef_bar_par_jour=benef_bar, autre_recette_par_jour=autre_recette,
        duree_soiree=duree_s, duree_journee=duree_j, duree_deux_jours=duree_2,
        equipes_soiree=eq_s, equipes_journee=eq_j, equipes_deux_jours=eq_2,
    )

    tournois = calc_tournois(tparams)

    st.divider()
    st.markdown("### Résultats annuels")
    colA, colB, colC, colD = st.columns(4)
    with colA:
        st.metric("Adhésions", euros(base["recettes_adhesions"]))
    with colB:
        st.metric("Réservations (hors adh)", euros(base["recettes_reservations"]))
    with colC:
        st.metric("Bénéfice net tournois", euros(tournois["annuel"]["benefice_net"]))
    with colD:
        total = base["total_hors_tournois"] + tournois["annuel"]["benefice_net"]
        st.metric("Total annuel (net)", euros(total))

    with st.expander("Détails des calculs"):
        st.write(f"Réservations annuelles = {base['reservations_annuelles']:,.0f} (pistes) × {JOUEURS_PAR_PISTE} joueurs = **{base['joueurs_totaux']:,.0f}** joueurs")
        st.write("Recettes réservations = Joueurs × [ p_adh × Prix_adh + (1 - p_adh) × Prix_non_adh ]")
        st.write(f"Tournois — recette brute annuelle = {euros(tournois['annuel']['recette_brute'])}")
        st.write(f"Tournois — dépenses annuelles = {euros(tournois['annuel']['depenses'])}")
        st.write(f"Tournois — recettes annexes (bar/repas) = {euros(tournois['annuel']['recettes_annexes'])}")
        st.write(f"Tournois — bénéfice net annuel = {euros(tournois['annuel']['benefice_net'])}")

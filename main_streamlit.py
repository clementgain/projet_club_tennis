import streamlit as st

st.set_page_config(page_title="Estimation recettes Padel", page_icon="🎾", layout="centered")
st.title("🎾 Estimation des recettes annuelles — 2 pistes de Padel")
st.caption("Chaque réservation correspond à **1h30** et **4 joueurs**. Calculs sur **365 jours/an**.")

st.subheader("Adhésions (recettes fixes)")
col1, col2 = st.columns(2)
with col1:
    prix_adh_tennis = st.number_input(
        "Prix de l'adhésion Padel si déjà adhérent Tennis (€)",
        min_value=0.0, step=10.0, value=50.0, format="%.2f",
        help="Montant payé par un adhérent Tennis pour ajouter l'option Padel."
    )
    nb_adh_tennis = st.number_input(
        "Nombre d'adhérents Padel déjà adhérents Tennis",
        min_value=0, step=1, value=40,
        help="Combien d'adhérents Tennis prendront l'option Padel."
    )
with col2:
    prix_adh_seul = st.number_input(
        "Prix de l'adhésion Padel seul (€)",
        min_value=0.0, step=10.0, value=120.0, format="%.2f",
        help="Montant pour une adhésion Padel sans adhésion Tennis."
    )
    nb_adh_seul = st.number_input(
        "Nombre d'adhérents Padel seul",
        min_value=0, step=1, value=30,
        help="Combien de personnes prendront une adhésion Padel sans être adhérents Tennis."
    )

st.divider()
st.subheader("Réservations (recettes variables)")
col3, col4 = st.columns(2)
with col3:
    prix_resa_adh = st.number_input(
        "Prix de la réservation 1h30 — adhérent (par joueur) (€)",
        min_value=0.0, step=1.0, value=6.0, format="%.2f",
        help="Prix payé par un adhérent, pour 1h30, par joueur."
    )
    nb_pistes_par_jour = st.slider(
        "Nombre moyen de pistes réservées par jour (toutes pistes confondues)",
        min_value=0.0, max_value=48.0, value=10.0, step=0.5,
        help=(
            "Total quotidien de créneaux réservés. "
            "Ex: si vous avez 2 pistes ouvertes 12h/jour avec créneaux de 1h30, "
            "le maximum théorique est 2 * (12 / 1,5) = 16 créneaux."
        )
    )
with col4:
    prix_resa_nonadh = st.number_input(
        "Prix de la réservation 1h30 — non adhérent (par joueur) (€)",
        min_value=0.0, step=1.0, value=10.0, format="%.2f",
        help="Prix payé par un non adhérent, pour 1h30, par joueur."
    )
    prop_adh_resa = st.slider(
        "Proportion d'adhérents dans les réservations",
        min_value=0.0, max_value=1.0, value=0.6, step=0.05,
        help="Part des joueurs réservant qui sont adhérents (entre 0 et 1)."
    )

# Constantes
JOUEURS_PAR_PISTE = 4
JOURS_PAR_AN = 365

# Calculs
recettes_adhesions = prix_adh_tennis * nb_adh_tennis + prix_adh_seul * nb_adh_seul

reservations_annuelles = nb_pistes_par_jour * JOURS_PAR_AN
joueurs_totaux = reservations_annuelles * JOUEURS_PAR_PISTE

recettes_resa_adh = joueurs_totaux * prop_adh_resa * prix_resa_adh
recettes_resa_nonadh = joueurs_totaux * (1 - prop_adh_resa) * prix_resa_nonadh
recettes_reservations = recettes_resa_adh + recettes_resa_nonadh

recettes_totales = recettes_adhesions + recettes_reservations

st.divider()
st.subheader("Résultats")
colA, colB, colC = st.columns(3)
with colA:
    st.metric("Recettes adhésions / an", f"{recettes_adhesions:,.0f} €")
with colB:
    st.metric("Recettes réservations / an", f"{recettes_reservations:,.0f} €",
              help="Calcul au prorata adhérents / non adhérents, 4 joueurs par réservation.")
with colC:
    st.metric("Recettes totales / an", f"{recettes_totales:,.0f} €")

with st.expander("Détails des calculs"):
    st.write(
        f"Réservations annuelles = {nb_pistes_par_jour} × {JOURS_PAR_AN} = **{reservations_annuelles:,.0f}**"
    )
    st.write(
        f"Joueurs totaux (par réservations) = {reservations_annuelles:,.0f} × {JOUEURS_PAR_PISTE} = **{joueurs_totaux:,.0f}**"
    )
    st.write(
        "Recettes réservations = Joueurs × [ p_adh × Prix_adh + (1 - p_adh) × Prix_non_adh ]"
    )
    st.write(
        f"➡️ {joueurs_totaux:,.0f} × [ {prop_adh_resa:.2f} × {prix_resa_adh:.2f} + (1 - {prop_adh_resa:.2f}) × {prix_resa_nonadh:.2f} ] = **{recettes_reservations:,.2f} €**"
    )
    st.write(
        f"Recettes adhésions = ({prix_adh_tennis:.2f} × {nb_adh_tennis}) + ({prix_adh_seul:.2f} × {nb_adh_seul}) = **{recettes_adhesions:,.2f} €**"
    )
    st.write(
        f"\n**Recettes totales / an** = **{recettes_totales:,.2f} €**"
    )

st.info(
    "💡 Conseil : jouez avec la proportion d'adhérents et le volume de réservations pour tester différents scénarios de remplissage.")

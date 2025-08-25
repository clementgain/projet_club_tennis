from math import ceil
from dataclasses import dataclass

JOUEURS_PAR_EQUIPE = 2
JOUEURS_PAR_PISTE = 4
JOURS_PAR_AN = 365
DEFAULT_COURTS = 2

@dataclass
class BaseInputs:
    prix_adh_tennis: float
    nb_adh_tennis: int
    prix_adh_seul: float
    nb_adh_seul: int
    prix_resa_adh: float
    prix_resa_nonadh: float
    nb_pistes_reservees_par_jour: float  # total toutes pistes
    proportion_adh_resa: float           # 0..1

@dataclass
class TournoiParams:
    # Fréquences annuelles
    n_soirees: int
    n_journees: int
    n_deux_jours: int
    # Prix
    prix_joueur_soiree: float
    prix_joueur_journee: float
    prix_joueur_deux_jours: float
    # Capacités
    equipes_soiree: int = 8
    equipes_journee: int = 12
    equipes_deux_jours: int = 20
    # Durées (en jours)
    duree_soiree: float = 0.5
    duree_journee: float = 1.0
    duree_deux_jours: float = 2.0
    # Dépenses unitaires
    ja_cout_par_jour: float = 50.0
    droit_enregistrement: float = 40.0
    balles_tubes_par_jour: int = 16
    balles_prix_par_tube: float = 5.0
    # Recettes annexes
    benef_bar_par_jour: float = 150.0
    autre_recette_par_jour: float = 0.0


def euros(x: float) -> str:
    return f"{x:,.0f} €".replace(",", " ")


def calc_reservations_annuelles(nb_pistes_reservees_par_jour: float) -> float:
    return nb_pistes_reservees_par_jour * JOURS_PAR_AN


def calc_recettes_base(inp: BaseInputs):
    """Recettes adhésions + réservations (prorata adh/non-adh)."""
    recettes_adhesions = inp.prix_adh_tennis * inp.nb_adh_tennis + inp.prix_adh_seul * inp.nb_adh_seul
    reservations_annuelles = calc_reservations_annuelles(inp.nb_pistes_reservees_par_jour)
    joueurs_totaux = reservations_annuelles * JOUEURS_PAR_PISTE
    recettes_resa = (
        joueurs_totaux * (inp.proportion_adh_resa * inp.prix_resa_adh + (1 - inp.proportion_adh_resa) * inp.prix_resa_nonadh)
    )
    total = recettes_adhesions + recettes_resa
    return {
        "recettes_adhesions": recettes_adhesions,
        "reservations_annuelles": reservations_annuelles,
        "joueurs_totaux": joueurs_totaux,
        "recettes_reservations": recettes_resa,
        "total_hors_tournois": total,
    }


def _tournoi_unitaire(equipes: int, prix_joueur: float, duree_jours: float, p: TournoiParams):
    joueurs = equipes * JOUEURS_PAR_EQUIPE
    recette_brute = joueurs * prix_joueur
    cout_balles = ceil(p.balles_tubes_par_jour * duree_jours) * p.balles_prix_par_tube
    cout_ja = p.ja_cout_par_jour * duree_jours
    cout_droits = p.droit_enregistrement
    depenses = cout_balles + cout_ja + cout_droits
    recettes_annexes = (p.benef_bar_par_jour + p.autre_recette_par_jour) * duree_jours
    benefice_net = recette_brute - depenses + recettes_annexes
    return {
        "joueurs": joueurs,
        "recette_brute": recette_brute,
        "depenses": depenses,
        "recettes_annexes": recettes_annexes,
        "benefice_net": benefice_net,
        "detail_couts": {
            "balles": cout_balles,
            "juge_arbitre": cout_ja,
            "droits": cout_droits,
        },
        "duree_jours": duree_jours,
    }


def calc_tournois(params: TournoiParams):
    soiree = _tournoi_unitaire(params.equipes_soiree, params.prix_joueur_soiree, params.duree_soiree, params)
    journee = _tournoi_unitaire(params.equipes_journee, params.prix_joueur_journee, params.duree_journee, params)
    deux_jours = _tournoi_unitaire(params.equipes_deux_jours, params.prix_joueur_deux_jours, params.duree_deux_jours, params)

    total = {
        "recette_brute": soiree["recette_brute"] * params.n_soirees
                         + journee["recette_brute"] * params.n_journees
                         + deux_jours["recette_brute"] * params.n_deux_jours,
        "depenses": soiree["depenses"] * params.n_soirees
                   + journee["depenses"] * params.n_journees
                   + deux_jours["depenses"] * params.n_deux_jours,
        "recettes_annexes": soiree["recettes_annexes"] * params.n_soirees
                           + journee["recettes_annexes"] * params.n_journees
                           + deux_jours["recettes_annexes"] * params.n_deux_jours,
        "benefice_net": soiree["benefice_net"] * params.n_soirees
                       + journee["benefice_net"] * params.n_journees
                       + deux_jours["benefice_net"] * params.n_deux_jours,
    }

    return {
        "unitaire": {
            "soiree": soiree,
            "journee": journee,
            "deux_jours": deux_jours,
        },
        "annuel": total,
    }


def capacity_reservations_per_day(open_hours: float, courts: int = DEFAULT_COURTS, slot_hours: float = 1.5) -> int:
    return int((open_hours // slot_hours) * courts)


# --- Scénarios de comparaison ---
@dataclass
class ScenarioAdhesionIllimitee:
    prix_adhesion_unique: float  # ~140
    nb_adherents: int
    prix_non_adh_resa: float     # ~7 €/joueur
    nb_resa_jour: float
    proportion_adh_resa: float   # part des joueurs qui sont adhérents

@dataclass
class ScenarioLocationPourTous:
    prix_resa_joueur: float
    nb_resa_jour: float


def calc_scenario_adhesion(s: ScenarioAdhesionIllimitee):
    reservations_annuelles = calc_reservations_annuelles(s.nb_resa_jour)
    joueurs_totaux = reservations_annuelles * JOUEURS_PAR_PISTE
    # Les adhérents ne paient pas les créneaux
    joueurs_payants = joueurs_totaux * (1 - s.proportion_adh_resa)
    recettes_resa = joueurs_payants * s.prix_non_adh_resa
    recettes_adh = s.prix_adhesion_unique * s.nb_adherents
    total = recettes_adh + recettes_resa
    return {
        "reservations_annuelles": reservations_annuelles,
        "joueurs_totaux": joueurs_totaux,
        "joueurs_payants": joueurs_payants,
        "recettes_reservations": recettes_resa,
        "recettes_adhesions": recettes_adh,
        "total_hors_tournois": total,
    }


def calc_scenario_location(s: ScenarioLocationPourTous):
    reservations_annuelles = calc_reservations_annuelles(s.nb_resa_jour)
    joueurs_totaux = reservations_annuelles * JOUEURS_PAR_PISTE
    recettes_resa = joueurs_totaux * s.prix_resa_joueur
    return {
        "reservations_annuelles": reservations_annuelles,
        "joueurs_totaux": joueurs_totaux,
        "recettes_reservations": recettes_resa,
        "total_hors_tournois": recettes_resa,
    }


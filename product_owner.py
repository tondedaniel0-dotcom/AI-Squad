from memory_store import formater_contexte
from models import ProfilAgent, ReponseAgent, RevisionAgent


def analyser(
    probleme: str,
    lecons_individuelles: list[dict[str, object]] | None = None,
    lecons_communes: list[dict[str, object]] | None = None,
    profil: ProfilAgent | None = None,
) -> ReponseAgent:
    contexte_memoire = formater_contexte(lecons_individuelles, lecons_communes)
    proposition = (
        f"Pour '{probleme}', prioriser le parcours qui apporte une valeur "
        "immédiate aux utilisateurs : rechercher, comparer, réserver et confirmer "
        "sans étape inutile. Limiter le MVP à ces actions, définir un indicateur "
        "de réussite et différer les fonctionnalités dont l'impact n'est pas "
        "mesuré."
    )
    if contexte_memoire:
        proposition += (
            " Le périmètre doit rester lié aux besoins validés "
            "et aux objectifs métier."
        )
    if profil is not None and profil.niveau_prudence >= 4:
        proposition += (
            " Chaque option différée devra conserver un coût de reprise limité."
        )
    return ReponseAgent(
        role="Product Owner",
        proposition=proposition,
        risques=[
            "Un périmètre trop large peut retarder la validation de la valeur.",
            "Une fonctionnalité attractive peut être peu utilisée.",
            "Des objectifs contradictoires peuvent disperser l'équipe.",
        ],
        confiance=0.9,
    )


def reviser(
    reponse: ReponseAgent,
    autres_reponses: list[ReponseAgent],
    profil: ProfilAgent | None = None,
) -> RevisionAgent:
    justification = (
        f"Révision effectuée après lecture de {len(autres_reponses)} "
        "propositions et arbitrage du périmètre."
    )
    if profil is not None and profil.niveau_prudence >= 4:
        justification += (
            " Les critères de valeur, les besoins utilisateurs et le retour "
            "sur investissement restent prioritaires."
        )
    return RevisionAgent(
        role=reponse.role,
        action="modifier",
        proposition=(
            f"{reponse.proposition} Mesurer le taux de conversion, "
            "le temps de réservation et la valeur par utilisateur avant "
            "d'étendre les fonctionnalités."
        ),
        risques=reponse.risques,
        objections=[
            "Une fonctionnalité ne doit pas être ajoutée sans utilisateur cible "
            "ni bénéfice observable.",
        ],
        confiance=0.9,
        justification=justification,
    )

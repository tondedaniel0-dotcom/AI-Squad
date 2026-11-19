from memory_store import formater_contexte
from models import ProfilAgent, ReponseAgent, RevisionAgent


def analyser(
    probleme: str,
    lecons_individuelles: list[dict[str, object]] | None = None,
    lecons_communes: list[dict[str, object]] | None = None,
    profil: ProfilAgent | None = None,
    recherche: dict[str, object] | None = None,
) -> ReponseAgent:
    contexte_memoire = formater_contexte(lecons_individuelles, lecons_communes)
    proposition = (
        f"Pour '{probleme}', formaliser les acteurs, les cas d'usage, les règles "
        "métier et les critères d'acceptation. Associer chaque besoin à un "
        "indicateur observable, un responsable, une donnée attendue et une valeur "
        "mesurable."
    )
    if contexte_memoire:
        proposition += (
            " Les règles non vérifiables doivent être clarifiées "
            "avant toute implémentation."
        )
    if profil is not None and profil.niveau_prudence >= 4:
        proposition += (
            " Toute hypothèse doit rester distinguée d'une exigence confirmée."
        )
    if recherche is not None and recherche.get("enabled"):
        nombre_sources = len(recherche.get("sources", []))
        if nombre_sources:
            proposition += (
                f" Les exigences peuvent être appuyées par {nombre_sources} "
                "source(s) traçable(s)."
            )
    return ReponseAgent(
        role="Business Analyst",
        proposition=proposition,
        risques=[
            "Un besoin ambigu peut produire une implémentation correcte mais inutile.",
            "Une règle métier implicite peut créer des résultats incohérents.",
            "Une valeur non mesurée peut empêcher de confirmer l’impact.",
        ],
        confiance=0.88,
    )


def reviser(
    reponse: ReponseAgent,
    autres_reponses: list[ReponseAgent],
    profil: ProfilAgent | None = None,
) -> RevisionAgent:
    justification = (
        f"Révision effectuée après lecture de {len(autres_reponses)} "
        "propositions et vérification des besoins métier."
    )
    if profil is not None and profil.niveau_prudence >= 4:
        justification += (
            " Les règles, les acteurs et les indicateurs doivent rester vérifiables."
        )
    return RevisionAgent(
        role=reponse.role,
        action="modifier",
        proposition=(
            f"{reponse.proposition} Chaque cas d'usage doit inclure "
            "ses données d'entrée, ses règles, ses exceptions, son résultat "
            "attendu et son indicateur de valeur."
        ),
        risques=reponse.risques,
        objections=[
            "Une fonctionnalité ne peut être validée sans règle métier "
            "ni critère d'acceptation observable.",
        ],
        confiance=0.88,
        justification=justification,
    )

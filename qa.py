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
        f"Avant toute validation du problème '{probleme}', j'établis les critères "
        "bloquants : résultat attendu, cas d'erreur, comportement limite et "
        "absence de régression. Les tests doivent être reliés à ces critères."
    )
    if contexte_memoire:
        proposition += " J'ajoute explicitement les chemins d'échec au plan de validation."
    if profil is not None and profil.niveau_prudence >= 5:
        proposition += " Chaque scénario doit disposer d'une preuve vérifiable."
    return ReponseAgent(
        role="QA",
        proposition=proposition,
        risques=[
            "Les scénarios de test peuvent manquer des comportements inattendus.",
            "Des tests insuffisants peuvent laisser passer des régressions.",
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
        "réponses d'agents."
    )
    if profil is not None and profil.niveau_prudence >= 5:
        justification += " Je maintiens un seuil d'acceptation explicite avant toute livraison."
    return RevisionAgent(
        role=reponse.role,
        action="modifier",
        proposition=(
            f"{reponse.proposition} Les tests doivent couvrir les choix "
            "d'architecture et le comportement du MVP."
        ),
        risques=reponse.risques,
        objections=[
            "Une proposition ne peut être retenue sans critères d'acceptation "
            "vérifiables."
        ],
        confiance=0.9,
        justification=justification,
    )
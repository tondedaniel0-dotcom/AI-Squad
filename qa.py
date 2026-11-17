from memory_store import formater_contexte
from models import ReponseAgent, RevisionAgent


def analyser(
    probleme: str,
    lecons_individuelles: list[dict[str, object]] | None = None,
    lecons_communes: list[dict[str, object]] | None = None,
) -> ReponseAgent:
    contexte_memoire = formater_contexte(lecons_individuelles, lecons_communes)
    proposition = (
        f"Pour le problème '{probleme}', définir les cas d'erreur et écrire "
        "les tests dès le début afin d'éviter les régressions."
    )
    if contexte_memoire:
        proposition += f" Leçons prises en compte : {contexte_memoire}."
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
) -> RevisionAgent:
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
        justification=(
            f"Révision effectuée après lecture de {len(autres_reponses)} "
            "réponses d'agents."
        ),
    )
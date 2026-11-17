from memory_store import formater_contexte
from models import ReponseAgent, RevisionAgent


def analyser(
    probleme: str,
    lecons_individuelles: list[dict[str, object]] | None = None,
    lecons_communes: list[dict[str, object]] | None = None,
) -> ReponseAgent:
    contexte_memoire = formater_contexte(lecons_individuelles, lecons_communes)
    proposition = (
        f"Pour le problème '{probleme}', produire rapidement un MVP fonctionnel "
        "en Python, puis ajouter les fonctionnalités progressivement."
    )
    if contexte_memoire:
        proposition += f" Leçons prises en compte : {contexte_memoire}."
    return ReponseAgent(
        role="Développeur",
        proposition=proposition,
        risques=[
            "Le MVP pourrait nécessiter une refactorisation avant la mise en production.",
            "Une implémentation rapide peut laisser des cas limites non traités.",
        ],
        confiance=0.8,
    )


def reviser(
    reponse: ReponseAgent,
    autres_reponses: list[ReponseAgent],
) -> RevisionAgent:
    return RevisionAgent(
        role=reponse.role,
        action="modifier",
        proposition=(
            f"{reponse.proposition} L'implémentation doit tenir compte des "
            "contraintes d'architecture et des scénarios de test."
        ),
        risques=reponse.risques,
        objections=[
            "Une solution rapide doit rester testable et suffisamment évolutive."
        ],
        confiance=0.8,
        justification=(
            f"Révision effectuée après lecture de {len(autres_reponses)} "
            "réponses d'agents."
        ),
    )
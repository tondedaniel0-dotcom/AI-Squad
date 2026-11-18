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
        f"Livrons d'abord une première version fonctionnelle du problème "
        f"'{probleme}' : découper l'implémentation en unités vérifiables, "
        "commencer par le parcours principal en Python, puis intégrer les "
        "fonctionnalités périphériques au fil des résultats."
    )
    if contexte_memoire:
        proposition += " Je découpe aussi les jalons de façon à détecter rapidement les écarts avant l'intégration."
    if profil is not None and profil.niveau_creativite >= 4:
        proposition += " Un prototype concret permettra d'éprouver rapidement les choix techniques."
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
    profil: ProfilAgent | None = None,
) -> RevisionAgent:
    justification = (
        f"Révision effectuée après lecture de {len(autres_reponses)} "
        "réponses d'agents."
    )
    if profil is not None and profil.niveau_prudence >= 3:
        justification += " Je garde une marge pour corriger l'implémentation après les premiers tests."
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
        justification=justification,
    )
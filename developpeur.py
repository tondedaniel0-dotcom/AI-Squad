from models import ReponseAgent


def analyser(probleme: str) -> ReponseAgent:
    return ReponseAgent(
        role="Développeur",
        proposition=(
            f"Pour le problème '{probleme}', produire rapidement un MVP fonctionnel "
            "en Python, puis ajouter les fonctionnalités progressivement."
        ),
        risques=[
            "Le MVP pourrait nécessiter une refactorisation avant la mise en production.",
            "Une implémentation rapide peut laisser des cas limites non traités.",
        ],
        confiance=0.8,
    )
from models import ReponseAgent


def analyser(probleme: str) -> ReponseAgent:
    return ReponseAgent(
        role="Architecte",
        proposition=(
            f"Pour résoudre le problème '{probleme}', commencer par une architecture "
            "simple, composée de composants réutilisables et séparant clairement "
            "les responsabilités."
        ),
        risques=[
            "Une architecture trop simple pourrait limiter les évolutions futures.",
            "Les besoins réels pourraient être incomplets ou mal compris.",
        ],
        confiance=0.85,
    )
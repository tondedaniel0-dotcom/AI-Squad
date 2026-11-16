from models import ReponseAgent


def analyser(probleme: str) -> ReponseAgent:
    return ReponseAgent(
        role="QA",
        proposition=(
            f"Pour le problème '{probleme}', définir les cas d'erreur et écrire "
            "les tests dès le début afin d'éviter les régressions."
        ),
        risques=[
            "Les scénarios de test peuvent manquer des comportements inattendus.",
            "Des tests insuffisants peuvent laisser passer des régressions.",
        ],
        confiance=0.9,
    )
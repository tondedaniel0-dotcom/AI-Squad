from models import ReponseAgent


def analyser(probleme: str) -> ReponseAgent:
    return ReponseAgent(
        role="Critique",
        proposition=(
            f"Concernant '{probleme}', vérifier les hypothèses, simplifier la "
            "solution et éviter le surdéveloppement."
        ),
        risques=[
            "Une simplification excessive peut omettre des besoins importants.",
            "Les hypothèses non vérifiées peuvent conduire à une mauvaise décision.",
        ],
        confiance=0.75,
    )
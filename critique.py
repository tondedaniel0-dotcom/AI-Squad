from models import ReponseAgent, RevisionAgent


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


def reviser(
    reponse: ReponseAgent,
    autres_reponses: list[ReponseAgent],
) -> RevisionAgent:
    return RevisionAgent(
        role=reponse.role,
        action="objection",
        proposition=reponse.proposition,
        risques=reponse.risques,
        objections=[
            "Les propositions doivent expliciter leurs hypothèses avant toute "
            "décision."
        ],
        confiance=0.75,
        justification=(
            f"Objection formulée après lecture de {len(autres_reponses)} "
            "réponses d'agents."
        ),
    )
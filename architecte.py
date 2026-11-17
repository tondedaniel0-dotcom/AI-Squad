from models import ReponseAgent, RevisionAgent


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


def reviser(
    reponse: ReponseAgent,
    autres_reponses: list[ReponseAgent],
) -> RevisionAgent:
    return RevisionAgent(
        role=reponse.role,
        action="modifier",
        proposition=(
            f"{reponse.proposition} La conception doit aussi intégrer les "
            "contraintes soulevées par les autres agents."
        ),
        risques=reponse.risques,
        objections=[
            "Les propositions doivent rester compatibles avec les contraintes "
            "d'implémentation et de validation."
        ],
        confiance=0.85,
        justification=(
            f"Révision effectuée après lecture de {len(autres_reponses)} "
            "réponses d'agents."
        ),
    )
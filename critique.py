from memory_store import formater_contexte
from models import ReponseAgent, RevisionAgent


def analyser(
    probleme: str,
    lecons_individuelles: list[dict[str, object]] | None = None,
    lecons_communes: list[dict[str, object]] | None = None,
) -> ReponseAgent:
    contexte_memoire = formater_contexte(lecons_individuelles, lecons_communes)
    proposition = (
        f"Concernant '{probleme}', vérifier les hypothèses, simplifier la "
        "solution et éviter le surdéveloppement."
    )
    if contexte_memoire:
        proposition += f" Leçons prises en compte : {contexte_memoire}."
    return ReponseAgent(
        role="Critique",
        proposition=proposition,
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
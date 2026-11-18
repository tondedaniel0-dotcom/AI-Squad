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
        f"Je remets en cause la proposition pour '{probleme}' avant toute "
        "validation : quelles hypothèses sont admises sans preuve, quel besoin "
        "reste incertain et quelle complexité pourrait être supprimée dès maintenant?"
    )
    if contexte_memoire:
        proposition += " Je cherche également les décisions prises sur des bases trop générales."
    if profil is not None and profil.niveau_prudence >= 5:
        proposition += " Toute conclusion non étayée doit être identifiée comme hypothèse."
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
    profil: ProfilAgent | None = None,
) -> RevisionAgent:
    justification = (
        f"Objection formulée après lecture de {len(autres_reponses)} "
        "réponses d'agents."
    )
    if profil is not None and profil.niveau_prudence >= 5:
        justification += " Je demande une preuve avant d'accepter cette modification."
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
        justification=justification,
    )
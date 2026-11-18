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
        f"Je structure la réponse au problème '{probleme}' autour de trois "
        "limites clairement définies : une séparation nette des responsabilités, "
        "des composants réutilisables et un chemin d'évolution explicite."
    )
    if contexte_memoire:
        proposition += " Les interfaces internes seront définies avant les composants afin d'éviter les changements tardifs."
    if profil is not None and profil.niveau_prudence >= 4:
        proposition += " Je privilégie des frontières stables avant d'ajouter des options nouvelles."
    return ReponseAgent(
        role="Architecte",
        proposition=proposition,
        risques=[
            "Une architecture trop simple pourrait limiter les évolutions futures.",
            "Les besoins réels pourraient être incomplets ou mal compris.",
        ],
        confiance=0.85,
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
    if profil is not None and profil.niveau_prudence >= 4:
        justification += " Les interfaces et les dépendances doivent rester réversibles."
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
        justification=justification,
    )
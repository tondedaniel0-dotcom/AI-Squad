from memory_store import formater_contexte
from models import ProfilAgent, ReponseAgent, RevisionAgent


def analyser(
    probleme: str,
    lecons_individuelles: list[dict[str, object]] | None = None,
    lecons_communes: list[dict[str, object]] | None = None,
    profil: ProfilAgent | None = None,
    recherche: dict[str, object] | None = None,
) -> ReponseAgent:
    contexte_memoire = formater_contexte(lecons_individuelles, lecons_communes)
    proposition = (
        f"Pour '{probleme}', définir un parcours de déploiement automatisé avec "
        "Infrastructure as Code, CI/CD, environnements séparés, sauvegardes "
        "vérifiées, supervision, alertes, rollback automatique et dimensionnement "
        "selon l'utilisation réelle."
    )
    if contexte_memoire:
        proposition += (
            " Les procédures opérationnelles doivent être testées "
            "avant la mise en production."
        )
    if profil is not None and profil.niveau_prudence >= 5:
        proposition += (
            " Toute dépendance manuelle ou procédure non reproductible "
            "doit être traitée comme un risque."
        )
    if recherche is not None and recherche.get("enabled"):
        domaines = sorted({
            str(source.get("domain", ""))
            for source in recherche.get("sources", [])
            if source.get("domain")
        })
        if domaines:
            proposition += (
                " Les pratiques opérationnelles peuvent être vérifiées auprès de "
                + ", ".join(domaines)
                + "."
            )
    return ReponseAgent(
        role="DevOps",
        proposition=proposition,
        risques=[
            "Une procédure manuelle peut produire une configuration différente.",
            "Sans sauvegarde testée, une panne peut provoquer une perte de données.",
            "Une absence d'observabilité ralentit la détection et la reprise.",
            "Un surdimensionnement peut augmenter durablement les coûts cloud.",
        ],
        confiance=0.92,
    )


def reviser(
    reponse: ReponseAgent,
    autres_reponses: list[ReponseAgent],
    profil: ProfilAgent | None = None,
) -> RevisionAgent:
    justification = (
        f"Révision effectuée après lecture de {len(autres_reponses)} "
        "propositions et vérification de l'exploitabilité."
    )
    if profil is not None and profil.niveau_prudence >= 5:
        justification += (
            " Le déploiement, les sauvegardes, les alertes et le rollback "
            "doivent rester vérifiables."
        )
    return RevisionAgent(
        role=reponse.role,
        action="objection",
        proposition=reponse.proposition,
        risques=reponse.risques,
        objections=[
            "Une mise en production doit disposer d'un rollback automatisé "
            "et d'une restauration de sauvegarde testée.",
            "Les ressources doivent être dimensionnées selon les mesures "
            "réelles et supervisées pour limiter les coûts.",
        ],
        confiance=0.92,
        justification=justification,
    )

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
        f"Pour '{probleme}', définir une séparation stricte des rôles et des "
        "permissions, avec une isolation serveur du tenant SaaS sur chaque "
        "requête. Exiger une authentification robuste, une autorisation vérifiée "
        "avant chaque action, des sessions révoquables et le chiffrement des "
        "données sensibles au repos et en transit."
    )
    if contexte_memoire:
        proposition += (
            " Le contrôle d'accès devra être testé sur les ressources croisées "
            "et les fonctions administratives."
        )
    if profil is not None and profil.niveau_prudence >= 5:
        proposition += (
            " Toute confiance dans les données utilisateur ou dans le tenant "
            "courant doit être évitée."
        )
    if recherche is not None and recherche.get("enabled"):
        domaines = sorted({
            str(source.get("domain", ""))
            for source in recherche.get("sources", [])
            if source.get("domain")
        })
        if domaines:
            proposition += (
                " Les éléments sécurité peuvent être vérifiés auprès de "
                + ", ".join(domaines)
                + "."
            )
    return ReponseAgent(
        role="Security",
        proposition=proposition,
        risques=[
            "Une autorisation insuffisante peut exposer les données d'un autre locataire.",
            "Une séparation des rôles trop permissive peut permettre des actions administratives.",
            "Des sessions mal protégées ou réutilisées peuvent entraîner une prise de compte.",
        ],
        confiance=0.95,
    )


def reviser(
    reponse: ReponseAgent,
    autres_reponses: list[ReponseAgent],
    profil: ProfilAgent | None = None,
) -> RevisionAgent:
    justification = (
        f"Révision effectuée après lecture de {len(autres_reponses)} "
        "propositions et vérification des interactions entre rôles."
    )
    if profil is not None and profil.niveau_prudence >= 5:
        justification += (
            " Les permissions, la frontière multi-tenant et la protection "
            "des données restent des préconditions."
        )
    return RevisionAgent(
        role=reponse.role,
        action="objection",
        proposition=reponse.proposition,
        risques=reponse.risques,
        objections=[
            "Chaque opération doit vérifier le tenant courant et les permissions "
            "de l'utilisateur côté serveur.",
            "Les données sensibles doivent être minimisées, chiffrées et protégées "
            "contre les exports non autorisés.",
        ],
        confiance=0.95,
        justification=justification,
    )

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
        f"Du point de vue de l'utilisateur confronté à '{probleme}', je propose "
        "un parcours court avec une intention principale visible à chaque écran, "
        "une navigation mobile simple, des actions faciles à atteindre et des "
        "messages d'erreur compréhensibles. Je vérifie aussi le clavier, le focus, "
        "le contraste et les erreurs auprès des parcours les plus défavorisés."
    )
    if contexte_memoire:
        proposition += " Je fais valider les décisions les plus importantes sur les parcours courants et défavorisés."
    if profil is not None and profil.niveau_creativite >= 5:
        proposition += " Je propose plusieurs variantes du parcours avant de figer l'interface."
    return ReponseAgent(
        role="Designer",
        proposition=proposition,
        risques=[
            "Un parcours trop long peut augmenter l'abandon avant la confirmation.",
            "Une interface non testée sur mobile peut provoquer des débordements "
            "ou rendre les actions difficiles à atteindre.",
            "Des composants sans sémantique ou sans focus visible peuvent exclure "
            "les utilisateurs de clavier et de lecteurs d'écran.",
        ],
        confiance=0.88,
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
    if profil is not None and profil.niveau_creativite >= 5:
        justification += " Cette révision conserve plusieurs possibilités de parcours pour les tester avec les utilisateurs."
    return RevisionAgent(
        role=reponse.role,
        action="modifier",
        proposition=(
            f"{reponse.proposition} Après lecture des autres analyses, "
            "documenter les critères UX dans les tests : parcours nominal en "
            "trois étapes, navigation clavier complète, affichage mobile sans "
            "débordement et messages d'erreur compréhensibles."
        ),
        risques=reponse.risques,
        objections=[
            "Une architecture ou un MVP ne doit pas repousser les critères "
            "d'accessibilité et de responsive design à une phase ultérieure."
        ],
        confiance=0.88,
        justification=justification,
    )

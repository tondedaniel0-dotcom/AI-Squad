from models import ReponseAgent, RevisionAgent


def analyser(probleme: str) -> ReponseAgent:
    return ReponseAgent(
        role="Designer",
        proposition=(
            f"Pour '{probleme}', concevoir un parcours en trois étapes : "
            "accueil, action principale et confirmation, avec un seul bouton "
            "d'action principal par écran. Utiliser une approche mobile-first, "
            "des mises en page fluides sans défilement horizontal et des zones "
            "tactiles d'au moins 44 px. Rendre chaque champ accessible au clavier, "
            "avec un libellé explicite, un focus visible, un contraste d'au moins "
            "4,5:1 et des erreurs affichées directement près du champ concerné."
        ),
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
) -> RevisionAgent:
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
        justification=(
            f"Révision effectuée après lecture de {len(autres_reponses)} "
            "réponses d'agents."
        ),
    )

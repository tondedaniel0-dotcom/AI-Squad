from models import ProfilAgent


PROFILS_AGENT = {
    "Architecte": ProfilAgent(
        role="Architecte",
        style="structuré et synthétique",
        niveau_creativite=3,
        niveau_prudence=4,
        specialite="architecture logicielle",
    ),
    "Développeur": ProfilAgent(
        role="Développeur",
        style="concret et orienté livraison",
        niveau_creativite=4,
        niveau_prudence=3,
        specialite="implémentation",
    ),
    "QA": ProfilAgent(
        role="QA",
        style="rigoureux et orienté vérification",
        niveau_creativite=2,
        niveau_prudence=5,
        specialite="qualité logicielle",
    ),
    "Critique": ProfilAgent(
        role="Critique",
        style="analytique et sceptique",
        niveau_creativite=3,
        niveau_prudence=5,
        specialite="remise en question",
    ),
    "Designer": ProfilAgent(
        role="Designer",
        style="empathique et orienté utilisateur",
        niveau_creativite=5,
        niveau_prudence=3,
        specialite="UX/UI",
    ),
    "Security": ProfilAgent(
        role="Security",
        style="précis, prudent et orienté menaces",
        niveau_creativite=2,
        niveau_prudence=5,
        specialite="sécurité applicative",
    ),
    "Product Owner": ProfilAgent(
        role="Product Owner",
        style="clair, stratégique et orienté arbitrage",
        niveau_creativite=4,
        niveau_prudence=4,
        specialite="stratégie produit",
    ),
}


def obtenir_profil(role: str) -> ProfilAgent:
    try:
        return PROFILS_AGENT[role]
    except KeyError as exc:
        raise ValueError(f"Profil inconnu pour le rôle : {role}") from exc


def formater_profil(profil: ProfilAgent) -> str:
    if not 1 <= profil.niveau_creativite <= 5:
        raise ValueError("Le niveau de créativité doit être compris entre 1 et 5.")
    if not 1 <= profil.niveau_prudence <= 5:
        raise ValueError("Le niveau de prudence doit être compris entre 1 et 5.")
    return (
        f"Style {profil.style}; créativité {profil.niveau_creativite}/5; "
        f"prudence {profil.niveau_prudence}/5; spécialité {profil.specialite}"
    )

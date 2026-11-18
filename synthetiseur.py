import re

from models import RevisionAgent, Synthese


_POINTS_ACCORD = {
    "Une approche progressive avec un MVP": {
        "commencer",
        "progressivement",
        "mvp",
    },
    "Une solution simple et maîtrisée": {
        "simple",
        "simplifier",
        "surdéveloppement",
    },
    "La validation par les tests": {
        "tests",
        "régressions",
    },
    "Un parcours utilisateur simple et accessible": {
        "parcours",
        "simple",
        "accessible",
    },
    "Une interface adaptée au mobile": {
        "mobile-first",
        "mobile",
        "responsive",
    },
    "La sécurité et l'isolation des locataires doivent être garanties": {
        "sécurité",
        "authentification",
        "autorisation",
        "tenant",
        "locataire",
        "permissions",
    },
    "La valeur produit doit être priorisée": {
        "valeur",
        "utilisateur",
        "mvp",
        "priorit",
        "roi",
        "objectif",
        "périmètre",
    },
}

_RISQUES_COMMUNS = {
    "Les besoins ou hypothèses pourraient être mal validés": {
        "besoins",
        "hypothèses",
    },
    "La couverture des cas limites pourrait être insuffisante": {
        "cas",
        "scénarios",
        "inattendus",
        "régressions",
    },
    "Les contraintes de validation doivent être résolues": {
        "validation",
        "testable",
        "critères",
        "tests",
    },
    "L'accessibilité et l'affichage responsive doivent être vérifiés": {
        "accessibilité",
        "clavier",
        "mobile",
        "débordement",
    },
}


def _mots(texte: str) -> set[str]:
    return set(re.findall(r"[a-zàâçéèêëîïôûùüÿœ-]+", texte.lower()))


def _themes_communs(
    textes_par_agent: list[set[str]],
    themes: dict[str, set[str]],
) -> list[str]:
    resultats = []
    for theme, mots_cles in themes.items():
        nombre_d_agents = sum(bool(mots & mots_cles) for mots in textes_par_agent)
        if nombre_d_agents >= 2:
            resultats.append(theme)
    return resultats


def synthetiser(revisions: list[RevisionAgent]) -> Synthese:
    if not revisions:
        raise ValueError("Impossible de produire une synthèse sans révision d'agent.")

    propositions = [_mots(revision.proposition) for revision in revisions]
    risques = [
        _mots(" ".join(revision.risques + revision.objections))
        for revision in revisions
    ]
    points_accord = _themes_communs(propositions, _POINTS_ACCORD)
    risques_communs = _themes_communs(risques, _RISQUES_COMMUNS)
    objections = [
        f"{revision.role} : {objection}"
        for revision in revisions
        for objection in revision.objections
    ]

    recommandation = (
        "Construire un MVP en Python avec une architecture simple et évolutive, "
        "puis valider les hypothèses et les cas limites avec des tests dès le début."
    )
    if objections:
        recommandation += (
            " Les objections soulevées doivent être traitées avant de figer "
            "l'architecture."
        )

    return Synthese(
        points_accord=points_accord,
        risques_communs=risques_communs,
        objections=objections,
        confiance_moyenne=sum(r.confiance for r in revisions) / len(revisions),
        recommandation=recommandation,
    )

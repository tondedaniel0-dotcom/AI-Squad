import re

from models import ReponseAgent, Synthese


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


def synthetiser(reponses: list[ReponseAgent]) -> Synthese:
    if not reponses:
        raise ValueError("Impossible de produire une synthèse sans réponse d'agent.")

    propositions = [_mots(reponse.proposition) for reponse in reponses]
    risques = [_mots(" ".join(reponse.risques)) for reponse in reponses]
    points_accord = _themes_communs(propositions, _POINTS_ACCORD)
    risques_communs = _themes_communs(risques, _RISQUES_COMMUNS)

    recommandation = (
        "Construire un MVP en Python avec une architecture simple et évolutive, "
        "puis valider les hypothèses et les cas limites avec des tests dès le début."
    )

    return Synthese(
        points_accord=points_accord,
        risques_communs=risques_communs,
        confiance_moyenne=sum(r.confiance for r in reponses) / len(reponses),
        recommandation=recommandation,
    )

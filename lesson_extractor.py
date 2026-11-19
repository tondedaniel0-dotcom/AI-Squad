import hashlib
from typing import Any

from memory_store import MemoryStore
from models import RevisionAgent, Synthese


def _id_lecon(role: str, probleme: str, contenu: str) -> str:
    valeur = f"{role}|{probleme}|{contenu}".encode("utf-8")
    return hashlib.sha1(valeur).hexdigest()[:12]


def _lecon(role: str, probleme: str, contenu: str, confiance: float) -> dict[str, Any]:
    return {
        "id": _id_lecon(role, probleme, contenu),
        "agent": role,
        "contenu": contenu,
        "source": "synthese_finale",
        "probleme": probleme,
        "confiance": confiance,
    }


def extraire_lecons(
    probleme: str,
    revisions: list[RevisionAgent],
    synthese: Synthese,
) -> dict[str, dict[str, Any]]:
    revisions_par_role = {
        revision.role: revision
        for revision in revisions
    }

    lignes_agent = {
        "Architecte": "Conserver une architecture simple, séparée en responsabilités "
                       "réutilisables et évolutive.",
        "Développeur": "Démarrer par un MVP fonctionnel, limiter l'étendue initiale "
                       "et préparer les cas limites pour l'évolution.",
        "QA": "Définir les critères d'acceptation, les cas d'erreur et les tests "
              "de régression avant de figer l'implémentation.",
        "Critique": "Expliciter les hypothèses, challenger la complexité et conserver "
                    "les objections jusqu'à leur résolution.",
        "Designer": "Concevoir un parcours simple, une interface responsive, "
                    "accessible au clavier et conforme aux besoins mobile.",
        "Security": "Séparer les rôles, isoler chaque tenant SaaS, contrôler "
                     "les permissions côté serveur et protéger les données.",
        "Product Owner": "Prioriser les besoins utilisateur, mesurer la valeur "
                         "métier et limiter le périmètre du MVP.",
        "DevOps": "Utiliser CI/CD, IaC, des sauvegardes testées, un rollback "
                   "automatisé et des dimensions cloud basées sur l'utilisation.",
        "Business Analyst": "Associer chaque besoin métier à une règle, "
                             "un indicateur, un acteur et un critère d'acceptation.",
    }

    lecons = {}
    for role, contenu in lignes_agent.items():
        revision = revisions_par_role.get(role)
        confiance = revision.confiance if revision is not None else synthese.confiance_moyenne
        lecons[role] = _lecon(role, probleme, contenu, confiance)

    risques = (
        "; ".join(synthese.risques_communs)
        if synthese.risques_communs
        else "Aucun risque commun explicite"
    )
    accords = (
        "; ".join(synthese.points_accord)
        if synthese.points_accord
        else "Aucun point d'accord explicite"
    )
    contenu_commune = (
        f"{synthese.recommandation} Points d'accord : {accords}. "
        f"Risques communs : {risques}."
    )
    analyse = synthese.analyse_consensus
    if analyse is not None:
        convergences = "; ".join(
            f"{item.theme} ({item.taux:.0%}, {item.niveau})"
            for item in analyse.convergences
        )
        desaccords = "; ".join(
            f"{item.theme} ({len(item.agents_support)} agents)"
            for item in analyse.desaccords
        )
        contenu_commune += (
            f" Consensus thématique : {analyse.taux_global:.0%}. "
            f"Convergences : {convergences or 'aucune'}. "
            f"Désaccords : {desaccords or 'aucun'}."
        )
    lecons["commun"] = _lecon(
        "Equipe",
        probleme,
        contenu_commune,
        synthese.confiance_moyenne,
    )
    return lecons


def sauvegarder_lecons(
    probleme: str,
    revisions: list[RevisionAgent],
    synthese: Synthese,
    store: MemoryStore | None = None,
) -> dict[str, dict[str, Any]]:
    store = store or MemoryStore()
    lecons = extraire_lecons(probleme, revisions, synthese)

    for role in (
        "Architecte",
        "Développeur",
        "QA",
        "Critique",
        "Designer",
        "Security",
        "Product Owner",
        "DevOps",
        "Business Analyst",
    ):
        store.ajouter_lecon(role, lecons[role])
    store.ajouter_lecon_commune(lecons["commun"])
    return lecons

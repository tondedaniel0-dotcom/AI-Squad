import re

from models import AnalyseConsensus, DesaccordTheme, RevisionAgent, ThemeConsensus


THEMES = {
    "Architecture et modularité": (
        "architecture", "structure", "composants", "modular",
        "responsabilités", "séparation",
    ),
    "MVP et livraison": (
        "mvp", "livr", "progressive", "implémentation", "livraison",
        "première version",
    ),
    "Qualité et tests": (
        "tests", "testable", "acceptation", "régression", "cas d'erreur",
        "validation", "preuve",
    ),
    "Expérience utilisateur": (
        "utilisateur", "parcours", "accessibilité", "responsive",
        "mobile", "interface", "ergonomie",
    ),
    "Sécurité": (
        "sécurité", "authentification", "autorisation", "permission",
        "permissions", "tenant", "locataire", "rbac", "chiffrement",
    ),
    "Valeur produit": (
        "valeur", "besoin", "utilisateur", "priorit", "roi",
        "mvp", "périmètre", "objectif",
    ),
    "Exploitation et fiabilité": (
        "déploiement", "ci/cd", "iac", "infra", "sauvegarde",
        "rollback", "observabilité", "monitoring", "disponibilité",
        "automatisation",
    ),
    "Coûts et FinOps": (
        "coût", "coûts", "finops", "dimensionnement", "cloud",
        "optimisation",
    ),
    "Besoin métier": (
        "besoin", "métier", "règle", "acteur", "cas d’usage",
        "cas d'usage", "indicateur", "acceptation",
    ),
}


RECOMMANDATIONS = {
    "Architecture et modularité":
        "Formaliser les responsabilités, les limites des composants et les interfaces.",
    "MVP et livraison":
        "Réduire le périmètre initial puis livrer de façon progressive et testable.",
    "Qualité et tests":
        "Définir les critères d'acceptation et automatiser les cas d'erreur avant la livraison.",
    "Expérience utilisateur":
        "Valider les parcours, l'accessibilité et le comportement responsive avec des utilisateurs.",
    "Sécurité":
        "Appliquer les contrôles d'autorisation côté serveur et isoler les données par tenant.",
    "Valeur produit":
        "Prioriser les besoins mesurant une valeur utilisateur ou métier explicite.",
    "Exploitation et fiabilité":
        "Préparer CI/CD, sauvegardes testées, observabilité et procédures de reprise.",
    "Coûts et FinOps":
        "Fixer des limites de coûts et mesurer l'utilisation avant toute optimisation prématurée.",
    "Besoin métier":
        "Associer chaque besoin à une règle, un acteur, un indicateur et un critère d'acceptation.",
}


def _normaliser(texte: str) -> str:
    return re.sub(r"\s+", " ", texte.lower()).strip()


def _soutient_theme(revision: RevisionAgent, mots: tuple[str, ...]) -> bool:
    texte = _normaliser(
        " ".join(
            [
                revision.proposition,
                *revision.risques,
                *revision.objections,
            ]
        )
    )
    return any(mot in texte for mot in mots)


def _niveau(taux: float) -> str:
    if taux >= 0.75:
        return "fort"
    if taux >= 0.5:
        return "majoritaire"
    if taux >= 0.34:
        return "faible"
    return "isolé"


def analyser_consensus(revisions: list[RevisionAgent]) -> AnalyseConsensus:
    if not revisions:
        raise ValueError("Impossible d'analyser un consensus sans révision d'agent.")

    total_agents = len(revisions)
    convergences: list[ThemeConsensus] = []
    desaccords: list[DesaccordTheme] = []
    recommandations: list[str] = []

    for theme, mots in THEMES.items():
        support = [
            revision.role
            for revision in revisions
            if _soutient_theme(revision, mots)
        ]
        taux = len(support) / total_agents
        niveau = _niveau(taux)

        if taux >= 0.5:
            convergence = ThemeConsensus(
                theme=theme,
                agents_support=support,
                taux=round(taux, 4),
                niveau=niveau,
                recommandation=RECOMMANDATIONS[theme],
            )
            convergences.append(convergence)
            recommandations.append(
                f"{theme} : {RECOMMANDATIONS[theme]}"
            )

        if 0.34 <= taux < 0.75:
            agents_opposes = [
                revision.role
                for revision in revisions
                if revision.role not in support
            ]
            objections = [
                objection
                for revision in revisions
                for objection in revision.objections
                if any(mot in _normaliser(objection) for mot in mots)
            ]
            desaccords.append(
                DesaccordTheme(
                    theme=theme,
                    agents_support=support,
                    agents_opposes=agents_opposes,
                    objections=objections,
                    niveau=niveau,
                    recommandation=RECOMMANDATIONS[theme],
                )
            )

    if convergences:
        taux_global = round(
            sum(convergence.taux for convergence in convergences)
            / len(convergences),
            4,
        )
    else:
        taux_global = 0.0

    points_non_resolus = [
        f"{desaccord.theme} : "
        f"{len(desaccord.agents_support)}/{total_agents} agents le prennent en compte"
        for desaccord in desaccords
    ]

    return AnalyseConsensus(
        convergences=convergences,
        desaccords=desaccords,
        taux_global=taux_global,
        points_non_resolus=points_non_resolus,
        recommandations=recommandations,
    )

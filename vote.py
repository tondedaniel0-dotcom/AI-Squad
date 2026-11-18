from models import ResultatVote, RevisionAgent, Vote


CRITERES_ROLE = {
    "Architecte": (
        ("architecture", ("architecture", "structure", "séparation")),
        ("modularité", ("composants", "modul", "réutilis")),
        ("responsabilités", ("responsabilités", "dépendances", "limites")),
        ("évolutivité", ("évolut", "progressive", "interfaces")),
        ("simplicité structurelle", ("simple", "claire", "surdéveloppement")),
    ),
    "Développeur": (
        ("faisabilité", ("implémentation", "fonctionnelle", "livr", "python")),
        ("MVP", ("mvp", "première version", "progressive")),
        ("implémentation", ("implémentation", "code", "composants")),
        ("maintenabilité", ("évolut", "refactor", "mainten")),
        ("simplicité technique", ("simple", "limite", "testable")),
    ),
    "QA": (
        ("critères d'acceptation", ("critères", "acceptation", "résultat")),
        ("cas d'erreur", ("cas d'erreur", "comportement limite", "échec")),
        ("régression", ("régression", "tests", "validation")),
        ("validation", ("preuve", "testable", "vérifiable")),
        ("preuves vérifiables", ("preuve", "critères", "vérif")),
    ),
    "Critique": (
        ("hypothèses explicites", ("hypothèses", "admises", "preuve")),
        ("gestion des risques", ("risque", "prudent", "limite")),
        ("objections", ("objection", "remets en cause", "désaccord")),
        ("qualité de l'argumentation", ("preuve", "pourquoi", "explicite")),
        ("réduction de la complexité", ("complexité", "simpl", "surdéveloppement")),
    ),
    "Designer": (
        ("parcours utilisateur", ("utilisateur", "parcours", "écran")),
        ("accessibilité", ("accessibilité", "clavier", "focus", "lecteurs")),
        ("responsive", ("responsive", "mobile", "débordement")),
        ("clarté", ("simple", "lisible", "compréhensible", "navigation")),
        ("feedback utilisateur", ("feedback", "erreur", "confirmation")),
    ),
    "Security": (
        ("authentification", ("authentification", "session", "connexion")),
        ("autorisation", ("autorisation", "permission", "rôle", "rbac")),
        ("contrôle des données", ("tenant", "locataire", "données", "isolation")),
        ("sécurité API", ("api", "idorr", "cors", "rate", "entrée")),
        ("chiffrement", ("chiffrement", "tls", "secret", "clé")),
    ),
    "Product Owner": (
        ("valeur métier", ("valeur", "bénéfice", "impact")),
        ("besoin utilisateur", ("utilisateur", "besoin", "usage")),
        ("priorisation", ("priorit", "p0", "p1", "périmètre")),
        ("MVP", ("mvp", "essentiel", "minimum")),
        ("ROI", ("roi", "coût", "revenu", "mesure")),
    ),
    "Product Owner": (
        ("valeur métier", ("valeur", "bénéfice", "impact")),
        ("besoin utilisateur", ("utilisateur", "besoin", "usage")),
        ("priorisation", ("priorit", "p0", "p1", "périmètre")),
        ("MVP", ("mvp", "essentiel", "minimum")),
        ("ROI", ("roi", "coût", "revenu", "mesure")),
    ),
}


POIDS_ROLE = {
    "Architecte": (0.30, 0.20, 0.20, 0.15, 0.15),
    "Développeur": (0.25, 0.20, 0.25, 0.15, 0.15),
    "QA": (0.25, 0.20, 0.20, 0.20, 0.15),
    "Critique": (0.20, 0.25, 0.20, 0.20, 0.15),
    "Designer": (0.25, 0.25, 0.15, 0.15, 0.20),
    "Security": (0.25, 0.25, 0.20, 0.15, 0.15),
    "Product Owner": (0.30, 0.25, 0.15, 0.15, 0.15),
    "Product Owner": (0.30, 0.25, 0.15, 0.15, 0.15),
}


def _texte_proposition(revision: RevisionAgent) -> str:
    return (
        revision.proposition
        + " "
        + " ".join(revision.risques)
        + " "
        + " ".join(revision.objections)
    ).lower()


def noter_proposition(votant: str, revision: RevisionAgent) -> tuple[float, dict[str, float]]:
    if votant not in CRITERES_ROLE:
        raise ValueError(f"Rôle inconnu : {votant}")

    texte = _texte_proposition(revision)
    notes = {}
    for nom, mots in CRITERES_ROLE[votant]:
        occurrences = sum(texte.count(mot) for mot in mots)
        notes[nom] = min(10.0, 4.0 + occurrences * 1.5)

    poids = POIDS_ROLE[votant]
    score = sum(
        note * poids[index]
        for index, note in enumerate(notes.values())
    )
    return round(min(10.0, score), 2), notes


def _choisir_candidat(
    votant: str,
    revisions: list[RevisionAgent],
) -> tuple[RevisionAgent, str, float]:
    evaluations = [
        (noter_proposition(votant, revision)[0], revision)
        for revision in revisions
    ]
    meilleur_score = max(score for score, _ in evaluations)
    meilleurs = [
        revision
        for score, revision in evaluations
        if abs(score - meilleur_score) < 1e-9
    ]
    minimum_objections = min(len(revision.objections) for revision in meilleurs)
    meilleurs = [
        revision
        for revision in meilleurs
        if len(revision.objections) == minimum_objections
    ]
    confiance_maximale = max(revision.confiance for revision in meilleurs)
    meilleurs = [
        revision
        for revision in meilleurs
        if abs(revision.confiance - confiance_maximale) < 1e-9
    ]
    candidat = max(meilleurs, key=lambda revision: revision.role)

    score, notes = noter_proposition(votant, candidat)
    critere_texte = ", ".join(
        CRITERES_ROLE[votant][index][0]
        for index in range(len(CRITERES_ROLE[votant]))
    )
    details = ", ".join(f"{nom}={note:.1f}/10" for nom, note in notes.items())
    justification = (
        f"J'ai évalué les sept propositions selon : {critere_texte}. "
        f"{candidat.role} obtient {score:.2f}/10 "
        f"(détails : {details}). "
        "Cette proposition est préférée pour sa meilleure note pondérée "
        "selon mon rôle."
    )
    if len(meilleurs) > 1:
        justification += " À égalité, je privilégie d'abord moins d'objections."
    return candidat, justification, score


def organiser_vote(revisions: list[RevisionAgent]) -> ResultatVote:
    if not revisions:
        raise ValueError("Impossible d'organiser un vote sans révision d'agent.")

    roles = [revision.role for revision in revisions]
    if len(set(roles)) != len(roles):
        raise ValueError("Chaque agent doit avoir un rôle unique pour voter.")

    votes = []
    for revision in revisions:
        candidat, justification, _ = _choisir_candidat(revision.role, revisions)
        votes.append(
            Vote(
                votant=revision.role,
                candidat=candidat.role,
                justification=justification,
            )
        )

    scores = {role: 0 for role in roles}
    for vote in votes:
        scores[vote.candidat] += 1

    score_maximal = max(scores.values())
    gagnants = [
        role for role, score in scores.items() if score == score_maximal
    ]

    return ResultatVote(
        votes=votes,
        scores=scores,
        gagnants=gagnants,
        taux_consensus=score_maximal / len(votes),
    )

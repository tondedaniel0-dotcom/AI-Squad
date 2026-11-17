from dataclasses import dataclass


@dataclass
class ReponseAgent:
    role: str
    proposition: str
    risques: list[str]
    confiance: float


@dataclass
class RevisionAgent:
    role: str
    action: str
    proposition: str
    risques: list[str]
    objections: list[str]
    confiance: float
    justification: str


@dataclass
class Vote:
    votant: str
    candidat: str


@dataclass
class ResultatVote:
    votes: list[Vote]
    scores: dict[str, int]
    gagnants: list[str]
    taux_consensus: float


@dataclass
class Synthese:
    points_accord: list[str]
    risques_communs: list[str]
    objections: list[str]
    confiance_moyenne: float
    recommandation: str

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
class ProfilAgent:
    role: str
    style: str
    niveau_creativite: int
    niveau_prudence: int
    specialite: str


@dataclass
class Vote:
    votant: str
    candidat: str
    justification: str


@dataclass
class ResultatVote:
    votes: list[Vote]
    scores: dict[str, int]
    gagnants: list[str]
    taux_consensus: float


@dataclass
class ThemeConsensus:
    theme: str
    agents_support: list[str]
    taux: float
    niveau: str
    recommandation: str = ""


@dataclass
class DesaccordTheme:
    theme: str
    agents_support: list[str]
    agents_opposes: list[str]
    objections: list[str]
    niveau: str
    recommandation: str = ""


@dataclass
class AnalyseConsensus:
    convergences: list[ThemeConsensus]
    desaccords: list[DesaccordTheme]
    taux_global: float
    points_non_resolus: list[str]
    recommandations: list[str]


@dataclass
class Synthese:
    points_accord: list[str]
    risques_communs: list[str]
    objections: list[str]
    confiance_moyenne: float
    recommandation: str
    analyse_consensus: AnalyseConsensus | None = None

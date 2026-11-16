from dataclasses import dataclass


@dataclass
class ReponseAgent:
    role: str
    proposition: str
    risques: list[str]
    confiance: float


@dataclass
class Synthese:
    points_accord: list[str]
    risques_communs: list[str]
    confiance_moyenne: float
    recommandation: str

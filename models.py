from dataclasses import dataclass


@dataclass
class ReponseAgent:
    role: str
    proposition: str
    risques: list[str]
    confiance: float

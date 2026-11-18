import json
from pathlib import Path
from typing import Any


AGENT_MEMORY_FILES = {
    "Architecte": "architecte.json",
    "Développeur": "developpeur.json",
    "QA": "qa.json",
    "Critique": "critique.json",
    "Designer": "designer.json",
}
COMMON_MEMORY_FILE = "lessons_learned.json"


def formater_contexte(
    lecons_individuelles: list[dict[str, Any]] | None,
    lecons_communes: list[dict[str, Any]] | None,
) -> str:
    contenus = []
    for lecons in (
        lecons_individuelles or [],
        lecons_communes or [],
    ):
        contenus.extend(
            str(lecon["contenu"])
            for lecon in lecons
            if isinstance(lecon.get("contenu"), str) and lecon["contenu"].strip()
        )
    return " ; ".join(contenus)


class MemoryStore:
    def __init__(self, memory_dir: str | Path = "memory") -> None:
        self.memory_dir = Path(memory_dir)
        self.initialiser()

    def initialiser(self) -> None:
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        for filename in [*AGENT_MEMORY_FILES.values(), COMMON_MEMORY_FILE]:
            chemin = self.memory_dir / filename
            if not chemin.exists():
                self._ecrire_json(chemin, [])

    def lire_agent(self, role: str) -> list[dict[str, Any]]:
        try:
            filename = AGENT_MEMORY_FILES[role]
        except KeyError as exc:
            raise ValueError(f"Rôle inconnu : {role}") from exc
        return self._lire_json(self.memory_dir / filename)

    def lire_commune(self) -> list[dict[str, Any]]:
        return self._lire_json(self.memory_dir / COMMON_MEMORY_FILE)

    def ajouter_lecon(self, role: str, lecon: dict[str, Any]) -> None:
        lecons = self.lire_agent(role)
        if any(
            element.get("id") == lecon.get("id")
            or (
                element.get("contenu") == lecon.get("contenu")
                and element.get("source") == lecon.get("source")
            )
            for element in lecons
        ):
            return
        lecons.append(self._valider_lecon(lecon))
        self._ecrire_json(self.memory_dir / AGENT_MEMORY_FILES[role], lecons)

    def ajouter_lecon_commune(self, lecon: dict[str, Any]) -> None:
        lecons = self.lire_commune()
        if any(
            element.get("id") == lecon.get("id")
            or (
                element.get("contenu") == lecon.get("contenu")
                and element.get("source") == lecon.get("source")
            )
            for element in lecons
        ):
            return
        lecons.append(self._valider_lecon(lecon))
        self._ecrire_json(self.memory_dir / COMMON_MEMORY_FILE, lecons)

    def _lire_json(self, chemin: Path) -> list[dict[str, Any]]:
        with chemin.open("r", encoding="utf-8") as fichier:
            contenu = json.load(fichier)
        if not isinstance(contenu, list) or not all(
            isinstance(element, dict) for element in contenu
        ):
            raise ValueError(f"Le fichier mémoire doit contenir une liste : {chemin}")
        return contenu

    @staticmethod
    def _valider_lecon(lecon: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(lecon, dict):
            raise TypeError("Une leçon doit être un objet JSON.")
        return lecon

    @staticmethod
    def _ecrire_json(chemin: Path, contenu: list[dict[str, Any]]) -> None:
        with chemin.open("w", encoding="utf-8") as fichier:
            json.dump(contenu, fichier, ensure_ascii=False, indent=2)
            fichier.write("\n")

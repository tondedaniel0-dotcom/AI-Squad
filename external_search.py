import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


class ExternalSearchService:
    def __init__(
        self,
        config_path: str | Path = "search_config.json",
        sources_path: str | Path = "search_sources.json",
        cache_path: str | Path = "search_cache.json",
    ) -> None:
        self.config_path = Path(config_path)
        self.sources_path = Path(sources_path)
        self.cache_path = Path(cache_path)
        self.config = self._charger_json(
            self.config_path,
            {
                "enabled": False,
                "provider": "local",
                "timeout_seconds": 5,
                "max_results": 5,
                "allowed_domains": [],
                "cache_enabled": True,
                "cache_ttl_seconds": 86400,
            },
        )
        self.sources = self._charger_json(self.sources_path, [])
        self.cache = self._charger_json(self.cache_path, [])
        self.initialiser_cache()

    def initialiser_cache(self) -> None:
        if not self.cache_path.exists():
            self._ecrire_json(self.cache_path, [])

    def rechercher(self, role: str, query: str) -> dict[str, Any]:
        if not self.config.get("enabled", False):
            return self._reponse_desactivee(role, query)

        query = query.strip()
        if not query:
            return self._reponse_erreur(role, query, "Requête vide.")

        cached = self._lire_cache(query, role)
        if cached is not None:
            cached["cache_hit"] = True
            return cached

        # Aucun appel Internet n'est effectué par ce prototype.
        # Le service ne retourne que des sources locales autorisées.
        resultats = []
        for source in self.sources:
            if not isinstance(source, dict):
                continue
            if not source.get("enabled", True):
                continue
            trust_score = float(source.get("trust_score", 0))
            if not 0 <= trust_score <= 1:
                continue
            if not self._source_autorisee(source):
                continue
            mots_requete = [
                mot
                for mot in query.lower().split()
                if len(mot) >= 3
            ]
            texte_source = " ".join(
                [
                    str(source.get("title", "")),
                    str(source.get("category", "")),
                    str(source.get("description", "")),
                ]
            ).lower()
            correspondances = sum(
                mot in texte_source
                for mot in mots_requete
            )
            if mots_requete and correspondances == 0:
                continue

            resultats.append(
                {
                    "title": source["title"],
                    "url": source["url"],
                    "domain": source["domain"],
                    "category": source["category"],
                    "trust_score": trust_score,
                    "snippet": source.get("description", ""),
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "provider": "local_allowlist",
                }
            )
            if len(resultats) >= int(self.config.get("max_results", 5)):
                break

        reponse = {
            "enabled": True,
            "role": role,
            "query": query,
            "results": resultats,
            "sources": resultats,
            "cache_hit": False,
            "error": None,
        }
        if self.config.get("cache_enabled", True):
            self._ecrire_cache(reponse)
        return reponse

    def _source_autorisee(self, source: dict[str, Any]) -> bool:
        domaine = str(source.get("domain", "")).lower()
        domaines_autorises = [
            str(item).lower()
            for item in self.config.get("allowed_domains", [])
        ]
        if domaines_autorises and domaine not in domaines_autorises:
            return False
        url = str(source.get("url", ""))
        return urlparse(url).scheme in ("http", "https") and urlparse(url).netloc

    def _lire_cache(self, query: str, role: str) -> dict[str, Any] | None:
        maintenant = datetime.now(timezone.utc)
        for entree in reversed(self.cache):
            if entree.get("query") != query or entree.get("role") != role:
                continue
            expires_at = entree.get("expires_at")
            if not expires_at:
                continue
            try:
                expiration = datetime.fromisoformat(expires_at)
            except ValueError:
                continue
            if expiration.tzinfo is None:
                expiration = expiration.replace(tzinfo=timezone.utc)
            if expiration > maintenant:
                return {
                    "enabled": True,
                    "role": role,
                    "query": query,
                    "results": entree.get("results", []),
                    "sources": entree.get("results", []),
                    "cache_hit": True,
                    "error": None,
                }
        return None

    def _ecrire_cache(self, reponse: dict[str, Any]) -> None:
        ttl = int(self.config.get("cache_ttl_seconds", 86400))
        entree = {
            "query": reponse["query"],
            "role": reponse["role"],
            "results": reponse["results"],
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(seconds=ttl)
            ).isoformat(),
        }
        if isinstance(self.cache, list):
            self.cache.append(entree)
            self._ecrire_json(self.cache_path, self.cache)

    def _reponse_desactivee(self, role: str, query: str) -> dict[str, Any]:
        return {
            "enabled": False,
            "role": role,
            "query": query,
            "results": [],
            "sources": [],
            "cache_hit": False,
            "error": "Recherche externe désactivée.",
        }

    def _reponse_erreur(
        self,
        role: str,
        query: str,
        message: str,
    ) -> dict[str, Any]:
        return {
            "enabled": bool(self.config.get("enabled", False)),
            "role": role,
            "query": query,
            "results": [],
            "sources": [],
            "cache_hit": False,
            "error": message,
        }

    @staticmethod
    def _charger_json(chemin: Path, valeur_par_defaut: Any) -> Any:
        if not chemin.exists():
            return valeur_par_defaut
        with chemin.open("r", encoding="utf-8") as fichier:
            return json.load(fichier)

    @staticmethod
    def _ecrire_json(chemin: Path, contenu: Any) -> None:
        chemin.parent.mkdir(parents=True, exist_ok=True)
        with chemin.open("w", encoding="utf-8") as fichier:
            json.dump(contenu, fichier, ensure_ascii=False, indent=2)

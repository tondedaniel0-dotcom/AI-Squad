import json
import tempfile
import unittest
from pathlib import Path

from external_search import ExternalSearchService


class ExternalSearchTests(unittest.TestCase):
    def creer_service(self, dossier: Path, enabled: bool = False) -> ExternalSearchService:
        config = {
            "enabled": enabled,
            "provider": "local",
            "timeout_seconds": 5,
            "max_results": 5,
            "allowed_domains": ["learn.microsoft.com", "owasp.org", "w3.org"],
            "cache_enabled": True,
            "cache_ttl_seconds": 86400,
        }
        sources = [
            {
                "title": "OWASP Top 10",
                "domain": "owasp.org",
                "url": "https://owasp.org/www-project-top-ten/",
                "category": "security",
                "trust_score": 0.98,
                "enabled": True,
                "description": "Risques de sécurité applicative.",
            },
            {
                "title": "Source interdite",
                "domain": "example.org",
                "url": "https://example.org/recherche",
                "category": "test",
                "trust_score": 1.0,
                "enabled": True,
                "description": "OWASP sécurité test.",
            },
        ]
        config_path = dossier / "search_config.json"
        sources_path = dossier / "search_sources.json"
        cache_path = dossier / "search_cache.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        sources_path.write_text(json.dumps(sources), encoding="utf-8")
        cache_path.write_text("[]", encoding="utf-8")
        return ExternalSearchService(config_path, sources_path, cache_path)

    def test_mode_off_par_defaut(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            service = self.creer_service(Path(dossier), False)
            reponse = service.rechercher("Security", "OWASP sécurité")
            self.assertFalse(reponse["enabled"])
            self.assertEqual(reponse["sources"], [])
            self.assertIn("désactivée", reponse["error"])

    def test_recherche_respecte_liste_blanche(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            service = self.creer_service(Path(dossier), True)
            reponse = service.rechercher("Security", "OWASP sécurité")
            self.assertTrue(reponse["enabled"])
            self.assertEqual(len(reponse["sources"]), 1)
            self.assertEqual(reponse["sources"][0]["domain"], "owasp.org")
            self.assertGreater(reponse["sources"][0]["trust_score"], 0.9)

    def test_requete_vide(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            service = self.creer_service(Path(dossier), True)
            reponse = service.rechercher("Architecte", " ")
            self.assertEqual(reponse["results"], [])
            self.assertIn("Requête vide", reponse["error"])

    def test_cache_recherche_repetee(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            service = self.creer_service(Path(dossier), True)
            premiere = service.rechercher("Architecte", "OWASP sécurité")
            deuxieme = service.rechercher("Architecte", "OWASP sécurité")
            self.assertFalse(premiere["cache_hit"])
            self.assertTrue(deuxieme["cache_hit"])


if __name__ == "__main__":
    unittest.main()

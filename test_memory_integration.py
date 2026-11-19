import tempfile
import unittest
from pathlib import Path

from architecte import analyser as analyser_architecte
from critique import analyser as analyser_critique
from developpeur import analyser as analyser_developpeur
from designer import analyser as analyser_designer
from memory_store import MemoryStore
from qa import analyser as analyser_qa
from security import analyser as analyser_security
from product_owner import analyser as analyser_product_owner
from devops import analyser as analyser_devops
from business_analyst import analyser as analyser_business_analyst
from devops import analyser as analyser_devops


ANALYSEURS = {
    "Architecte": analyser_architecte,
    "Développeur": analyser_developpeur,
    "QA": analyser_qa,
    "Critique": analyser_critique,
    "Designer": analyser_designer,
    "Security": analyser_security,
    "Product Owner": analyser_product_owner,
    "DevOps": analyser_devops,
    "Business Analyst": analyser_business_analyst,
}


class MemoryIntegrationTests(unittest.TestCase):
    def test_agents_repondent_avec_une_memoire_vide(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            lecons_communes = store.lire_commune()

            for role, analyser in ANALYSEURS.items():
                reponse = analyser(
                    "concevoir une application",
                    store.lire_agent(role),
                    lecons_communes,
                )
                self.assertNotIn("mémoire individuelle", reponse.proposition.lower())
                self.assertNotIn("mémoire commune", reponse.proposition.lower())

    def test_agents_integrent_les_lecons_individuelles_et_communes(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            for role in ANALYSEURS:
                store.ajouter_lecon(
                    role,
                    {"contenu": f"Leçon individuelle pour {role}"},
                )
            store.ajouter_lecon_commune(
                {"contenu": "Toujours vérifier les hypothèses."}
            )

            for role, analyser in ANALYSEURS.items():
                reponse_sans_memoire = analyser(
                    "concevoir une application",
                    [],
                    [],
                )
                reponse = analyser(
                    "concevoir une application",
                    store.lire_agent(role),
                    store.lire_commune(),
                )
                self.assertNotIn(f"Leçon individuelle pour {role}", reponse.proposition)
                self.assertNotIn("Toujours vérifier les hypothèses.", reponse.proposition)
                self.assertNotIn("Leçons prises en compte", reponse.proposition)
                self.assertGreater(len(reponse.proposition), 80)
                self.assertNotEqual(reponse_sans_memoire.proposition, reponse.proposition)


if __name__ == "__main__":
    unittest.main()

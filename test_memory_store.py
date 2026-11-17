import json
import tempfile
import unittest
from pathlib import Path

from memory_store import AGENT_MEMORY_FILES, COMMON_MEMORY_FILE, MemoryStore


class MemoryStoreTests(unittest.TestCase):
    def test_cree_les_fichiers_memoires_manquants(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            memory_dir = Path(dossier) / "memory"
            store = MemoryStore(memory_dir)

            fichiers_attendus = [
                *AGENT_MEMORY_FILES.values(),
                COMMON_MEMORY_FILE,
            ]
            self.assertTrue(all((memory_dir / nom).exists() for nom in fichiers_attendus))
            self.assertEqual(store.lire_agent("Architecte"), [])
            self.assertEqual(store.lire_commune(), [])

    def test_ecrit_et_relit_une_lecon_agent(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            lecon = {"contenu": "Tester les cas limites.", "confiance": 0.9}

            store.ajouter_lecon("QA", lecon)

            nouveau_store = MemoryStore(store.memory_dir)
            self.assertEqual(nouveau_store.lire_agent("QA"), [lecon])

    def test_ecrit_une_lecon_commune_en_json(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            lecon = {"contenu": "Commencer par un MVP."}

            store.ajouter_lecon_commune(lecon)

            chemin = store.memory_dir / COMMON_MEMORY_FILE
            with chemin.open("r", encoding="utf-8") as fichier:
                self.assertEqual(json.load(fichier), [lecon])


if __name__ == "__main__":
    unittest.main()

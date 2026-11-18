import tempfile
import unittest
from pathlib import Path

from lesson_extractor import extraire_lecons, sauvegarder_lecons
from memory_store import MemoryStore
from models import RevisionAgent, Synthese


def creer_revisions() -> list[RevisionAgent]:
    roles = (
        "Architecte",
        "Développeur",
        "QA",
        "Critique",
        "Designer",
        "Security",
        "Product Owner",
    )
    return [
        RevisionAgent(
            role=role,
            action="modifier",
            proposition=f"Proposition révisée de {role}",
            risques=["Risque commun"],
            objections=[],
            confiance=0.8,
            justification="Révision après débat",
        )
        for role in roles
    ]


def creer_synthese() -> Synthese:
    return Synthese(
        points_accord=["Approche progressive"],
        risques_communs=["Cas limites insuffisamment testés"],
        objections=["Vérifier les hypothèses"],
        confiance_moyenne=0.8,
        recommandation="Construire un MVP testable et accessible.",
    )


class LessonExtractorTests(unittest.TestCase):
    def test_extraire_sept_lecons(self) -> None:
        lecons = extraire_lecons(
            "concevoir une application",
            creer_revisions(),
            creer_synthese(),
        )

        self.assertEqual(
            set(lecons),
            {
                "Architecte",
                "Développeur",
                "QA",
                "Critique",
                "Designer",
                "Security",
                "Product Owner",
                "commun",
            },
        )
        self.assertEqual(lecons["QA"]["agent"], "QA")
        self.assertEqual(lecons["commun"]["agent"], "Equipe")

    def test_sauvegarder_et_ecrire_la_lecon_commune(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")

            sauvegarder_lecons(
                "concevoir une application",
                creer_revisions(),
                creer_synthese(),
                store,
            )

            self.assertEqual(len(store.lire_agent("Architecte")), 1)
            self.assertEqual(len(store.lire_agent("Développeur")), 1)
            self.assertEqual(len(store.lire_agent("QA")), 1)
            self.assertEqual(len(store.lire_agent("Critique")), 1)
            self.assertEqual(len(store.lire_agent("Designer")), 1)
            self.assertEqual(len(store.lire_agent("Security")), 1)
            self.assertEqual(len(store.lire_agent("Product Owner")), 1)
            self.assertEqual(len(store.lire_commune()), 1)

    def test_evitement_des_doublons(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            arguments = (
                "concevoir une application",
                creer_revisions(),
                creer_synthese(),
            )

            sauvegarder_lecons(*arguments, store)
            sauvegarder_lecons(*arguments, store)

            self.assertEqual(len(store.lire_agent("QA")), 1)
            self.assertEqual(len(store.lire_commune()), 1)


if __name__ == "__main__":
    unittest.main()

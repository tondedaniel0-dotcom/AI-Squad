import tempfile
import unittest
from pathlib import Path

from agent_profiles import obtenir_profil
from devops import analyser, reviser
from lesson_extractor import sauvegarder_lecons
from memory_store import MemoryStore
from memory_store import MemoryStore
from models import ReponseAgent, RevisionAgent, Synthese
from vote import organiser_vote


def revision(role: str, proposition: str, confiance: float) -> RevisionAgent:
    return RevisionAgent(
        role=role,
        action="modifier",
        proposition=proposition,
        risques=["Risque opérationnel"],
        objections=[],
        confiance=confiance,
        justification="Révision test",
    )


class DevOpsAgentTests(unittest.TestCase):
    def test_analyse_et_revision_devops(self) -> None:
        reponse = analyser(
            "SaaS de réservation",
            [],
            [],
            obtenir_profil("DevOps"),
        )
        self.assertIsInstance(reponse, ReponseAgent)
        self.assertEqual(reponse.role, "DevOps")
        self.assertIn("CI/CD", reponse.proposition)
        self.assertIn("rollback", reponse.proposition)

        revision = reviser(reponse, [], obtenir_profil("DevOps"))
        self.assertIsInstance(revision, RevisionAgent)
        self.assertEqual(revision.role, "DevOps")
        self.assertGreaterEqual(len(revision.objections), 1)

    def test_huit_votes_et_consensus(self) -> None:
        revisions = [
            revision("Architecte", "Architecture modulaire", 0.85),
            revision("Développeur", "MVP Python testable", 0.80),
            revision("QA", "Tests et cas d'erreur", 0.90),
            revision("Critique", "Hypothèses et preuves", 0.75),
            revision("Designer", "Parcours utilisateur accessible", 0.88),
            revision("Security", "RBAC et isolation du tenant", 0.95),
            revision("Product Owner", "MVP prioritaire avec ROI", 0.90),
            revision(
                "DevOps",
                "CI/CD, IaC, observabilité, sauvegardes, rollback et FinOps",
                0.92,
            ),
        ]
        resultat = organiser_vote(revisions)
        self.assertEqual(len(resultat.votes), 8)
        self.assertEqual(sum(resultat.scores.values()), 8)
        self.assertEqual(
            set(vote.votant for vote in resultat.votes),
            {
                "Architecte",
                "Développeur",
                "QA",
                "Critique",
                "Designer",
                "Security",
                "Product Owner",
                "DevOps",
            },
        )
        self.assertGreater(resultat.taux_consensus, 0)
        self.assertTrue(all(vote.justification for vote in resultat.votes))

    def test_memoire_devops_persiste(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            revisions = [
                revision(role, f"Proposition {role}", 0.85)
                for role in (
                    "Architecte",
                    "Développeur",
                    "QA",
                    "Critique",
                    "Designer",
                    "Security",
                    "Product Owner",
                )
            ]
            revisions.append(
                RevisionAgent(
                    "DevOps",
                    "objection",
                    "CI/CD, IaC, sauvegardes, rollback et monitoring.",
                    ["Panne opérationnelle"],
                    ["Tester régulièrement les restaurations."],
                    0.92,
                    "Révision DevOps",
                )
            )
            synthese = Synthese(
                points_accord=["Déploiement reproductible"],
                risques_communs=["Absence de rollback"],
                objections=["Tester les restaurations"],
                confiance_moyenne=0.88,
                recommandation="Déployer avec automatisation et observabilité.",
            )
            sauvegarder_lecons(
                "SaaS de réservation",
                revisions,
                synthese,
                store,
            )
            lecons = store.lire_agent("DevOps")
            self.assertGreaterEqual(len(lecons), 1)
            self.assertIn("ci/cd", lecons[-1]["contenu"].lower())


if __name__ == "__main__":
    unittest.main()

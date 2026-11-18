import tempfile
import unittest
from pathlib import Path

from agent_profiles import obtenir_profil
from lesson_extractor import sauvegarder_lecons
from memory_store import MemoryStore
from models import ReponseAgent, RevisionAgent, Synthese
from product_owner import analyser, reviser
from vote import organiser_vote


def creer_revision(role: str, proposition: str, confiance: float) -> RevisionAgent:
    return RevisionAgent(
        role=role,
        action="modifier",
        proposition=proposition,
        risques=["Risque SaaS"],
        objections=[],
        confiance=confiance,
        justification="Révision test",
    )


class ProductOwnerAgentTests(unittest.TestCase):
    def test_profil_analyse_et_revision(self) -> None:
        profil = obtenir_profil("Product Owner")
        reponse = analyser(
            "SaaS de réservation de terrains",
            [],
            [],
            profil,
        )
        self.assertIsInstance(reponse, ReponseAgent)
        self.assertEqual(reponse.role, "Product Owner")
        self.assertIn("valeur", reponse.proposition.lower())
        self.assertIn("mvp", reponse.proposition.lower())
        self.assertEqual(profil.niveau_creativite, 4)
        self.assertEqual(profil.niveau_prudence, 4)

        revision = reviser(reponse, [], profil)
        self.assertIsInstance(revision, RevisionAgent)
        self.assertEqual(revision.role, "Product Owner")
        self.assertIn("valeur", revision.proposition.lower())

    def test_demonstration_saas_avec_sept_agents(self) -> None:
        revisions = [
            creer_revision("Architecte", "Architecture modulaire", 0.85),
            creer_revision("Développeur", "MVP Python testable", 0.80),
            creer_revision("QA", "Critères d'acceptation et tests", 0.90),
            creer_revision("Critique", "Hypothèses explicites et preuves", 0.75),
            creer_revision(
                "Designer",
                "Parcours utilisateur accessible responsive",
                0.88,
            ),
            creer_revision(
                "Security",
                "RBAC, isolation du tenant et chiffrement",
                0.95,
            ),
            creer_revision(
                "Product Owner",
                "Réserver, payer et annuler avec une valeur utilisateur mesurée",
                0.90,
            ),
        ]

        resultat = organiser_vote(revisions)
        self.assertEqual(len(resultat.votes), 7)
        self.assertEqual(sum(resultat.scores.values()), 7)
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
            },
        )
        self.assertTrue(all(vote.justification for vote in resultat.votes))

    def test_memoire_product_owner(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            revisions = [
                creer_revision(role, f"Proposition {role}", 0.85)
                for role in (
                    "Architecte",
                    "Développeur",
                    "QA",
                    "Critique",
                    "Designer",
                    "Security",
                )
            ]
            revisions.append(
                RevisionAgent(
                    "Product Owner",
                    "modifier",
                    "Prioriser la réservation et mesurer la valeur.",
                    ["Périmètre"],
                    ["Limiter les fonctionnalités secondaires."],
                    0.90,
                    "Révision produit",
                )
            )
            synthese = Synthese(
                points_accord=["MVP prioritaire"],
                risques_communs=["Périmètre trop large"],
                objections=["Définir la valeur métier"],
                confiance_moyenne=0.87,
                recommandation="Construire un MVP centré sur la réservation.",
            )
            sauvegarder_lecons(
                "SaaS de réservation",
                revisions,
                synthese,
                store,
            )

            lecons = store.lire_agent("Product Owner")
            self.assertGreaterEqual(len(lecons), 1)
            self.assertIn("valeur", lecons[-1]["contenu"].lower())


if __name__ == "__main__":
    unittest.main()

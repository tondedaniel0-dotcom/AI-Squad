import tempfile
import unittest
from pathlib import Path

from agent_profiles import obtenir_profil
from business_analyst import analyser, reviser
from lesson_extractor import sauvegarder_lecons
from memory_store import MemoryStore
from models import ReponseAgent, RevisionAgent, Synthese
from vote import organiser_vote


def revision(role: str, proposition: str, confiance: float) -> RevisionAgent:
    return RevisionAgent(
        role=role,
        action="modifier",
        proposition=proposition,
        risques=["Risque métier"],
        objections=[],
        confiance=confiance,
        justification="Révision test",
    )


class BusinessAnalystAgentTests(unittest.TestCase):
    def test_profil_analyse_et_revision(self) -> None:
        profil = obtenir_profil("Business Analyst")
        reponse = analyser(
            "SaaS de réservation",
            [],
            [],
            profil,
        )
        self.assertIsInstance(reponse, ReponseAgent)
        self.assertEqual(reponse.role, "Business Analyst")
        self.assertIn("règles", reponse.proposition.lower())
        self.assertIn("indicateur", reponse.proposition.lower())
        self.assertEqual(profil.niveau_creativite, 3)
        self.assertEqual(profil.niveau_prudence, 4)

        revision = reviser(reponse, [], profil)
        self.assertIsInstance(revision, RevisionAgent)
        self.assertEqual(revision.role, "Business Analyst")
        self.assertGreaterEqual(len(revision.objections), 1)

    def test_neuf_votes_saas(self) -> None:
        revisions = [
            revision("Architecte", "Architecture modulaire", 0.85),
            revision("Développeur", "MVP Python testable", 0.80),
            revision("QA", "Critères d'acceptation et tests", 0.90),
            revision("Critique", "Hypothèses explicites et preuves", 0.75),
            revision("Designer", "Parcours utilisateur accessible", 0.88),
            revision("Security", "RBAC, tenant et chiffrement", 0.95),
            revision("Product Owner", "MVP centré sur la valeur", 0.90),
            revision("DevOps", "CI/CD, sauvegardes et rollback", 0.92),
            revision(
                "Business Analyst",
                "Règles métier, cas d’usage, indicateurs et acceptation",
                0.88,
            ),
        ]

        resultat = organiser_vote(revisions)
        self.assertEqual(len(resultat.votes), 9)
        self.assertEqual(sum(resultat.scores.values()), 9)
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
                "Business Analyst",
            },
        )
        self.assertTrue(all(vote.justification for vote in resultat.votes))

    def test_memoire_business_analyst(self) -> None:
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
                    "DevOps",
                )
            ]
            revisions.append(
                RevisionAgent(
                    "Business Analyst",
                    "modifier",
                    "Associer chaque réservation à une règle, un indicateur et un critère d'acceptation.",
                    ["Ambiguïté métier"],
                    ["Valider les règles avec les utilisateurs."],
                    0.88,
                    "Révision métier",
                )
            )
            synthese = Synthese(
                points_accord=["Besoin de réservation"],
                risques_communs=["Règles métier ambiguës"],
                objections=["Mesurer la valeur"],
                confiance_moyenne=0.87,
                recommandation="Construire un SaaS avec règles métier vérifiables.",
            )
            sauvegarder_lecons(
                "SaaS de réservation",
                revisions,
                synthese,
                store,
            )

            lecons = store.lire_agent("Business Analyst")
            self.assertGreaterEqual(len(lecons), 1)
            self.assertIn("règle", lecons[-1]["contenu"].lower())


if __name__ == "__main__":
    unittest.main()

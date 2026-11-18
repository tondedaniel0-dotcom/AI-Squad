import tempfile
import unittest
from pathlib import Path

from agent_profiles import obtenir_profil
from lesson_extractor import sauvegarder_lecons
from memory_store import MemoryStore
from models import ReponseAgent, RevisionAgent, Synthese
from security import analyser, reviser
from synthetiseur import synthetiser
from vote import organiser_vote


class SecurityAgentTests(unittest.TestCase):
    def test_security_analyse_et_revise(self) -> None:
        reponse = analyser(
            "SaaS de réservation multi-tenant",
            [],
            [],
            obtenir_profil("Security"),
        )
        self.assertIsInstance(reponse, ReponseAgent)
        self.assertEqual(reponse.role, "Security")
        self.assertIn("tenant", reponse.proposition.lower())
        self.assertIn("permissions", reponse.proposition.lower())

        revision = reviser(reponse, [], obtenir_profil("Security"))
        self.assertIsInstance(revision, RevisionAgent)
        self.assertEqual(revision.role, "Security")
        self.assertGreaterEqual(len(revision.objections), 1)

    def test_integration_complete_avec_six_agents(self) -> None:
        revisions = [
            RevisionAgent(
                role,
                "modifier",
                proposition,
                risques,
                objections,
                confiance,
                "Révision test",
            )
            for role, proposition, risques, objections, confiance in (
                (
                    "Architecte",
                    "Architecture simple avec composants séparés.",
                    ["Complexité"],
                    [],
                    0.85,
                ),
                (
                    "Développeur",
                    "MVP Python testable.",
                    ["Dette technique"],
                    [],
                    0.80,
                ),
                (
                    "QA",
                    "Tests, cas d'erreur et critères d'acceptation.",
                    ["Régression"],
                    [],
                    0.90,
                ),
                (
                    "Critique",
                    "Hypothèses explicites et réduction des risques.",
                    ["Hypothèses"],
                    [],
                    0.75,
                ),
                (
                    "Designer",
                    "Parcours utilisateur accessible et responsive.",
                    ["Ergonomie"],
                    [],
                    0.88,
                ),
                (
                    "Security",
                    "Authentification forte, autorisation RBAC, isolation du tenant "
                    "SaaS, contrôle d'accès et chiffrement des données.",
                    ["Exposition multi-tenant"],
                    ["Vérifier les permissions côté serveur."],
                    0.95,
                ),
            )
        ]

        resultat = organiser_vote(revisions)
        self.assertEqual(len(resultat.votes), 6)
        for vote in resultat.votes:
            self.assertTrue(vote.justification)
        self.assertEqual(sum(resultat.scores.values()), 6)
        self.assertEqual(set(resultat.scores), {
            "Architecte",
            "Développeur",
            "QA",
            "Critique",
            "Designer",
            "Security",
        })

    def test_lecon_security_en_memoire(self) -> None:
        with tempfile.TemporaryDirectory() as dossier:
            store = MemoryStore(Path(dossier) / "memory")
            revisions = [
                RevisionAgent(
                    role,
                    "modifier",
                    f"Proposition sécurité pour {role}",
                    ["Risques"],
                    [],
                    0.85,
                    "Révision test",
                )
                for role in (
                    "Architecte",
                    "Développeur",
                    "QA",
                    "Critique",
                    "Designer",
                )
            ]
            revisions.append(
                RevisionAgent(
                    "Security",
                    "objection",
                    "Contrôler les permissions RBAC et isoler chaque tenant.",
                    ["Exposition des données"],
                    ["Vérifier les permissions côté serveur."],
                    0.95,
                    "Objection sécurité",
                )
            )
            synthese = Synthese(
                points_accord=["Approche progressive"],
                risques_communs=["Isolation multi-tenant"],
                objections=["Contrôler les permissions"],
                confiance_moyenne=0.87,
                recommandation="Construire un SaaS avec sécurité, qualité et isolation.",
            )
            sauvegarder_lecons(
                "SaaS de réservation",
                revisions,
                synthese,
                store,
            )

            lecons = store.lire_agent("Security")
            self.assertGreaterEqual(len(lecons), 1)
            self.assertIn("tenant", lecons[-1]["contenu"].lower())

    def test_synthese_reconnait_la_securite(self) -> None:
        revisions = [
            RevisionAgent(
                role,
                "modifier",
                proposition,
                ["Risque"],
                [],
                0.85,
                "Révision test",
            )
            for role, proposition in (
                ("Architecte", "Architecture sécurisée tenant avec permissions"),
                ("Développeur", "MVP testable"),
                ("QA", "Tests et validation"),
                ("Critique", "Hypothèses et complexité"),
                ("Designer", "Parcours utilisateur"),
                (
                    "Security",
                    "Authentification, autorisation, tenant, permissions "
                    "et chiffrement.",
                ),
            )
        ]
        synthese = synthetiser(revisions)
        self.assertIsInstance(synthese, Synthese)
        security_found = any(
            "sécurité" in theme.lower() or "locataire" in theme.lower()
            for theme in synthese.points_accord + synthese.risques_communs
        )
        self.assertTrue(security_found)


if __name__ == "__main__":
    unittest.main()

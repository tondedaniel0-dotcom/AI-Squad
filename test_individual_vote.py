import unittest

from models import RevisionAgent
from vote import organiser_vote


def revision(
    role: str,
    proposition: str,
    confiance: float,
    risques: list[str] | None = None,
    objections: list[str] | None = None,
) -> RevisionAgent:
    return RevisionAgent(
        role=role,
        action="modifier",
        proposition=proposition,
        risques=risques or [],
        objections=objections or [],
        confiance=confiance,
        justification="Révision test",
    )


class IndividualVoteTests(unittest.TestCase):
    def test_cinq_agents_peuvent_voter_differemment(self) -> None:
        revisions = [
            revision(
                "Architecte",
                "Séparer les composants et définir les responsabilités.",
                0.85,
            ),
            revision(
                "Développeur",
                "Livrer rapidement un MVP avec une implémentation Python testable.",
                0.80,
            ),
            revision(
                "QA",
                "Définir les tests, les cas d'erreur, les critères d'acceptation "
                "et la régression.",
                0.90,
            ),
            revision(
                "Critique",
                "Vérifier les hypothèses avec des preuves et réduire les risques.",
                0.75,
                objections=["Une objection reste à traiter."],
            ),
            revision(
                "Designer",
                "Simplifier le parcours utilisateur, l'accessibilité, le responsive "
                "mobile et l'interface.",
                0.88,
            ),
        ]

        resultat = organiser_vote(revisions)

        candidats = [vote.candidat for vote in resultat.votes]
        self.assertGreater(len(set(candidats)), 1)
        self.assertNotEqual(candidats, ["QA"] * 5)
        self.assertTrue(all(vote.justification for vote in resultat.votes))
        self.assertEqual(sum(resultat.scores.values()), 5)
        self.assertGreater(resultat.taux_consensus, 0)

    def test_toutes_les_propositions_sont_evaluees(self) -> None:
        revisions = [
            revision(
                "Architecte",
                "Architecture simple, composants modulaire, responsabilités séparées.",
                0.85,
            ),
            revision(
                "Développeur",
                "MVP Python testable avec implémentation progressive.",
                0.80,
            ),
            revision(
                "QA",
                "Critères d'acceptation, tests, cas d'erreur, régression et preuves.",
                0.90,
            ),
            revision(
                "Critique",
                "Hypothèses explicites, risques, objections et réduction de la complexité.",
                0.75,
            ),
            revision(
                "Designer",
                "Parcours utilisateur accessible, responsive, clair avec feedback.",
                0.88,
            ),
        ]

        from vote import noter_proposition

        for votant in ("Architecte", "Développeur", "QA", "Critique", "Designer"):
            scores = [
                noter_proposition(votant, proposition)[0]
                for proposition in revisions
            ]
            self.assertEqual(len(scores), 5)
            self.assertTrue(all(0 <= score <= 10 for score in scores))

    def test_consensus_intermediaire_possible(self) -> None:
        revisions = [
            revision(
                "Architecte",
                "Architecture simple, composants, responsabilités et évolutivité.",
                0.85,
            ),
            revision(
                "Développeur",
                "Livraison rapide.",
                0.80,
            ),
            revision(
                "QA",
                "MVP Python testable avec implémentation progressive, maintenabilité, "
                "critères d'acceptation, tests, cas d'erreur, régression et preuves "
                "vérifiables.",
                0.90,
            ),
            revision(
                "Critique",
                "Hypothèses explicites, preuves, risques et objections.",
                0.75,
            ),
            revision(
                "Designer",
                "Parcours utilisateur, accessibilité responsive, clarté et feedback.",
                0.88,
            ),
        ]

        resultat = organiser_vote(revisions)

        self.assertGreater(resultat.taux_consensus, 0.2)
        self.assertLess(resultat.taux_consensus, 1.0)


if __name__ == "__main__":
    unittest.main()

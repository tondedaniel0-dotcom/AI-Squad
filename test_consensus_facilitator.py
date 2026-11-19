import unittest

from consensus_facilitator import analyser_consensus
from models import RevisionAgent


def revision(role: str, proposition: str, risques=None, objections=None) -> RevisionAgent:
    return RevisionAgent(
        role=role,
        action="modifier",
        proposition=proposition,
        risques=risques or [],
        objections=objections or [],
        confiance=0.85,
        justification="Révision test",
    )


def neuf_revisions() -> list[RevisionAgent]:
    return [
        revision("Architecte", "MVP progressif. Architecture simple avec composants séparés."),
        revision("Développeur", "MVP Python testable avec implémentation progressive."),
        revision("QA", "MVP progressif. Critères d'acceptation, tests, cas d'erreur et régression."),
        revision("Critique", "MVP progressif. Expliciter les hypothèses et réduire les risques."),
        revision("Designer", "MVP progressif. Parcours utilisateur accessible et responsive."),
        revision("Security", "MVP progressif. Authentification, autorisation RBAC, tenant et chiffrement."),
        revision("Product Owner", "MVP progressif. Prioriser la valeur utilisateur, le MVP et le ROI."),
        revision("DevOps", "MVP progressif. CI/CD, IaC, sauvegardes, rollback et observabilité."),
        revision("Business Analyst", "MVP progressif. Règles métier, besoins, indicateurs et acceptation."),
    ]


class ConsensusFacilitatorTests(unittest.TestCase):
    def test_neuf_agents_produisent_des_convergences(self) -> None:
        analyse = analyser_consensus(neuf_revisions())
        self.assertEqual(len(neuf_revisions()), 9)
        self.assertGreaterEqual(len(analyse.convergences), 1)
        self.assertTrue(all(convergence.agents_support for convergence in analyse.convergences))
        self.assertTrue(all(convergence.recommandation for convergence in analyse.convergences))

    def test_consensus_fort_et_repartition_correcte(self) -> None:
        revisions = neuf_revisions()
        analyse = analyser_consensus(revisions)
        convergence_testee = next(
            item for item in analyse.convergences
            if item.theme == "MVP et livraison"
        )
        self.assertGreaterEqual(len(convergence_testee.agents_support), 2)
        self.assertIn(convergence_testee.niveau, {"fort", "majoritaire"})

    def test_desaccords_detectes_par_theme(self) -> None:
        revisions = neuf_revisions()
        for index, role in (
            (1, "Développeur"),
            (6, "Product Owner"),
            (7, "DevOps"),
            (8, "Business Analyst"),
        ):
            revisions[index] = revision(
                role,
                "MVP progressif. FinOps, coûts cloud, optimisation et suivi.",
                ["Coût"],
                ["Limiter l'optimisation prématurée"],
            )
        analyse = analyser_consensus(revisions)
        themes = {desaccord.theme for desaccord in analyse.desaccords}
        self.assertIn("Coûts et FinOps", themes)
        cout = next(
            item for item in analyse.desaccords
            if item.theme == "Coûts et FinOps"
        )
        self.assertIn("DevOps", cout.agents_support)
        self.assertTrue(cout.recommandation)

    def test_recommandations_par_theme_presentes(self) -> None:
        analyse = analyser_consensus(neuf_revisions())
        self.assertGreater(len(analyse.recommandations), 0)
        self.assertEqual(
            len(analyse.recommandations),
            len(analyse.convergences),
        )

    def test_erreur_sans_revision(self) -> None:
        with self.assertRaises(ValueError):
            analyser_consensus([])

    def test_taux_global_compris_entre_zero_et_un(self) -> None:
        analyse = analyser_consensus(neuf_revisions())
        self.assertGreaterEqual(analyse.taux_global, 0.0)
        self.assertLessEqual(analyse.taux_global, 1.0)


if __name__ == "__main__":
    unittest.main()

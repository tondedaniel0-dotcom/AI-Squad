import unittest

from agent_profiles import PROFILS_AGENT, obtenir_profil
from architecte import analyser as analyser_architecte
from critique import analyser as analyser_critique
from developpeur import analyser as analyser_developpeur
from designer import analyser as analyser_designer
from qa import analyser as analyser_qa
from security import analyser as analyser_security
from product_owner import analyser as analyser_product_owner
from devops import analyser as analyser_devops
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
    "DevOps": analyser_devops,
}


class AgentProfileTests(unittest.TestCase):
    def test_huit_profils_complets(self) -> None:
        self.assertEqual(set(PROFILS_AGENT), set(ANALYSEURS))
        for profil in PROFILS_AGENT.values():
            self.assertTrue(profil.style)
            self.assertTrue(profil.specialite)
            self.assertIn(profil.niveau_creativite, range(1, 6))
            self.assertIn(profil.niveau_prudence, range(1, 6))

    def test_profils_influencent_reellement_le_style(self) -> None:
        for role, analyser in ANALYSEURS.items():
            sans_profil = analyser("concevoir une application")
            avec_profil = analyser(
                "concevoir une application",
                [],
                [],
                obtenir_profil(role),
            )
            self.assertNotEqual(sans_profil.proposition, avec_profil.proposition)
            self.assertNotIn("Approche professionnelle", avec_profil.proposition)
            self.assertNotIn("spécialité", avec_profil.proposition)
            self.assertNotIn("créativité", avec_profil.proposition)
            self.assertNotIn("prudence", avec_profil.proposition)
            self.assertNotIn("Leçons prises en compte", avec_profil.proposition)
            self.assertNotIn("mémoire individuelle", avec_profil.proposition.lower())
            self.assertNotIn("mémoire commune", avec_profil.proposition.lower())

    def test_differences_de_vocabulaire_entre_agents(self) -> None:
        propositions = {
            role: analyser(
                "concevoir une application",
                [],
                [],
                obtenir_profil(role),
            ).proposition
            for role, analyser in ANALYSEURS.items()
        }

        self.assertIn("structure", propositions["Architecte"].lower())
        self.assertIn("livrons", propositions["Développeur"].lower())
        self.assertIn("critères bloquants", propositions["QA"].lower())
        self.assertIn("remets en cause", propositions["Critique"].lower())
        self.assertIn("utilisateur", propositions["Designer"].lower())
        self.assertIn("tenant", propositions["Security"].lower())
        self.assertIn("valeur", propositions["Product Owner"].lower())
        self.assertIn("déploiement", propositions["DevOps"].lower())
        self.assertIn("déploiement", propositions["DevOps"].lower())


if __name__ == "__main__":
    unittest.main()

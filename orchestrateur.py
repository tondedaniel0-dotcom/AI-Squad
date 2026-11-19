from architecte import analyser as architecte
from architecte import reviser as reviser_architecte
from agent_profiles import obtenir_profil
from developpeur import analyser as developpeur
from developpeur import reviser as reviser_developpeur
from qa import analyser as qa
from qa import reviser as reviser_qa
from critique import analyser as critique
from critique import reviser as reviser_critique
from designer import analyser as designer
from designer import reviser as reviser_designer
from security import analyser as security
from security import reviser as reviser_security
from product_owner import analyser as product_owner
from product_owner import reviser as reviser_product_owner
from devops import analyser as devops
from devops import reviser as reviser_devops
from business_analyst import analyser as business_analyst
from business_analyst import reviser as reviser_business_analyst
from lesson_extractor import sauvegarder_lecons
from memory_store import MemoryStore
from synthetiseur import synthetiser
from vote import organiser_vote
from external_search import ExternalSearchService

probleme = input("Quel est le problème à analyser ? ")
memory_store = MemoryStore()
lecons_communes = memory_store.lire_commune()
search_service = ExternalSearchService()
search_architecte = search_service.rechercher(
    "Architecte",
    "architecture SaaS composants responsabilité évolutivité",
)
search_security = search_service.rechercher(
    "Security",
    "authentification autorisation isolation tenant sécurité API",
)
search_product_owner = search_service.rechercher(
    "Product Owner",
    "valeur MVP utilisateur priorisation ROI",
)

print("\n" + "=" * 50)

reponses = [
    architecte(
        probleme,
        memory_store.lire_agent("Architecte"),
        lecons_communes,
        obtenir_profil("Architecte"),
        search_architecte,
    ),
    developpeur(
        probleme,
        memory_store.lire_agent("Développeur"),
        lecons_communes,
        obtenir_profil("Développeur"),
    ),
    qa(
        probleme,
        memory_store.lire_agent("QA"),
        lecons_communes,
        obtenir_profil("QA"),
    ),
    critique(
        probleme,
        memory_store.lire_agent("Critique"),
        lecons_communes,
        obtenir_profil("Critique"),
    ),
    designer(
        probleme,
        memory_store.lire_agent("Designer"),
        lecons_communes,
        obtenir_profil("Designer"),
    ),
    security(
        probleme,
        memory_store.lire_agent("Security"),
        lecons_communes,
        obtenir_profil("Security"),
        search_security,
    ),
    product_owner(
        probleme,
        memory_store.lire_agent("Product Owner"),
        lecons_communes,
        obtenir_profil("Product Owner"),
    ),
    devops(
        probleme,
        memory_store.lire_agent("DevOps"),
        lecons_communes,
        obtenir_profil("DevOps"),
    ),
    business_analyst(
        probleme,
        memory_store.lire_agent("Business Analyst"),
        lecons_communes,
        obtenir_profil("Business Analyst"),
        search_product_owner,
    ),
]

for reponse in reponses:
    print(f"\n[{reponse.role}]")
    print(f"Proposition : {reponse.proposition}")
    print("Risques :")
    for risque in reponse.risques:
        print(f"- {risque}")
    print(f"Confiance : {reponse.confiance:.0%}")

revisions = [
    reviser_architecte(
        reponses[0],
        reponses[1:],
        obtenir_profil("Architecte"),
    ),
    reviser_developpeur(
        reponses[1],
        reponses[:1] + reponses[2:],
        obtenir_profil("Développeur"),
    ),
    reviser_qa(
        reponses[2],
        reponses[:2] + reponses[3:],
        obtenir_profil("QA"),
    ),
    reviser_critique(
        reponses[3],
        reponses[:3],
        obtenir_profil("Critique"),
    ),
    reviser_designer(
        reponses[4],
        reponses[:4],
        obtenir_profil("Designer"),
    ),
    reviser_security(
        reponses[5],
        reponses[:5],
        obtenir_profil("Security"),
    ),
    reviser_product_owner(
        reponses[6],
        reponses[:6],
        obtenir_profil("Product Owner"),
    ),
    reviser_devops(
        reponses[7],
        reponses[:7],
        obtenir_profil("DevOps"),
    ),
    reviser_business_analyst(
        reponses[8],
        reponses[:8],
        obtenir_profil("Business Analyst"),
    ),
]

print("\n" + "=" * 50)
print("DEUXIEME TOUR DE DEBAT")
for revision in revisions:
    print(f"\n[{revision.role}]")
    print(f"Action : {revision.action}")
    print(f"Proposition : {revision.proposition}")
    print("Risques :")
    for risque in revision.risques:
        print(f"- {risque}")
    print("Objections :")
    for objection in revision.objections:
        print(f"- {objection}")
    print(f"Confiance : {revision.confiance:.0%}")
    print(f"Justification : {revision.justification}")

print("\n" + "=" * 50)
print("VOTE")
resultat_vote = organiser_vote(revisions)
for vote in resultat_vote.votes:
    print(f"- {vote.votant} vote pour {vote.candidat}")
    print(f"  Justification : {vote.justification}")
print("\nRésultats :")
for role, score in resultat_vote.scores.items():
    print(f"- {role} : {score} vote(s)")
print(f"Gagnant(s) : {', '.join(resultat_vote.gagnants)}")
print(f"Taux de consensus : {resultat_vote.taux_consensus:.0%}")

print("\n" + "=" * 50)
print("SYNTHESE FINALE")
synthese = synthetiser(revisions)
print(f"\nConfiance moyenne : {synthese.confiance_moyenne:.0%}")
print(f"\nRecommandation : {synthese.recommandation}")

sauvegarder_lecons(probleme, revisions, synthese, memory_store)
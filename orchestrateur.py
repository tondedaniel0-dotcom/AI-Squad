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
from lesson_extractor import sauvegarder_lecons
from memory_store import MemoryStore
from synthetiseur import synthetiser
from vote import organiser_vote

probleme = input("Quel est le problème à analyser ? ")
memory_store = MemoryStore()
lecons_communes = memory_store.lire_commune()

print("\n" + "=" * 50)

reponses = [
    architecte(
        probleme,
        memory_store.lire_agent("Architecte"),
        lecons_communes,
        obtenir_profil("Architecte"),
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
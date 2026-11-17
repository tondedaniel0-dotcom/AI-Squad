from architecte import analyser as architecte
from architecte import reviser as reviser_architecte
from developpeur import analyser as developpeur
from developpeur import reviser as reviser_developpeur
from qa import analyser as qa
from qa import reviser as reviser_qa
from critique import analyser as critique
from critique import reviser as reviser_critique
from designer import analyser as designer
from designer import reviser as reviser_designer
from synthetiseur import synthetiser
from vote import organiser_vote

probleme = input("Quel est le problème à analyser ? ")

print("\n" + "=" * 50)

reponses = [
    architecte(probleme),
    developpeur(probleme),
    qa(probleme),
    critique(probleme),
    designer(probleme),
]

for reponse in reponses:
    print(f"\n[{reponse.role}]")
    print(f"Proposition : {reponse.proposition}")
    print("Risques :")
    for risque in reponse.risques:
        print(f"- {risque}")
    print(f"Confiance : {reponse.confiance:.0%}")

revisions = [
    reviser_architecte(reponses[0], reponses[1:]),
    reviser_developpeur(reponses[1], reponses[:1] + reponses[2:]),
    reviser_qa(reponses[2], reponses[:2] + reponses[3:]),
    reviser_critique(reponses[3], reponses[:3]),
    reviser_designer(reponses[4], reponses[:4]),
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
print("\nRésultats :")
for role, score in resultat_vote.scores.items():
    print(f"- {role} : {score} vote(s)")
print(f"Gagnant(s) : {', '.join(resultat_vote.gagnants)}")
print(f"Taux de consensus : {resultat_vote.taux_consensus:.0%}")

print("\n" + "=" * 50)
print("SYNTHESE FINALE")
synthese = synthetiser(revisions)
print("\nPoints d'accord :")
for point in synthese.points_accord:
    print(f"- {point}")
print("\nRisques communs :")
for risque in synthese.risques_communs:
    print(f"- {risque}")
print("\nObjections prises en compte :")
for objection in synthese.objections:
    print(f"- {objection}")
print(f"\nConfiance moyenne : {synthese.confiance_moyenne:.0%}")
print(f"\nRecommandation : {synthese.recommandation}")
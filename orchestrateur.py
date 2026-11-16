from architecte import analyser as architecte
from developpeur import analyser as developpeur
from qa import analyser as qa
from critique import analyser as critique

probleme = input("Quel est le problème à analyser ? ")

print("\n" + "=" * 50)

reponses = [
    architecte(probleme),
    developpeur(probleme),
    qa(probleme),
    critique(probleme),
]

for reponse in reponses:
    print(f"\n[{reponse.role}]")
    print(f"Proposition : {reponse.proposition}")
    print("Risques :")
    for risque in reponse.risques:
        print(f"- {risque}")
    print(f"Confiance : {reponse.confiance:.0%}")

print("\n" + "=" * 50)
print("DEBAT TERMINE")
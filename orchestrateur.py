from architecte import analyser as architecte
from developpeur import analyser as developpeur
from qa import analyser as qa
from critique import analyser as critique

probleme = input("Quel est le problème à analyser ? ")

print("\n" + "=" * 50)

print(architecte(probleme))
print(developpeur(probleme))
print(qa(probleme))
print(critique(probleme))

print("\n" + "=" * 50)
print("DEBAT TERMINE")
# fichier: salutation_sans_type.py

def saluer(nom, age):
    return "Salut " + nom + " ! Tu as " + str(age) + " ans."

# Test
msg = saluer("Bob", 30)
print(msg)
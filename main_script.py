# main_script.py (Contient des erreurs de style et de typage)

def calculate_sum(a, b):
    # Erreur de typage (pas de Type Hinting)
    # Erreur de style (espace manquant apres la virgule, nom de fonction snake_case)
    return a + b

def greeting(name):
    return "Hello " + name

# Problème de typage (ajout d'un int et d'un str)
total_result = calculate_sum(10, "5")

print(total_result)
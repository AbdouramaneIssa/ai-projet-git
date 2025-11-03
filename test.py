def saluer(nom: str, age: int) -> str:
    """
    Retourne un message de salutation personnalisé.
    
    Args:
        nom (str): Le prénom de la personne.
        age (int): L'âge de la personne.
    
    Returns:
        str: Le message complet.
    """
    return f"Bonjour {nom} ! Tu as {age} ans."

# Utilisation
message: str = saluer("Alice", 25)
print(message)
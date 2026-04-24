import re
from django.core.exceptions import ValidationError

def valider_mot_de_passe(password):
    erreurs = []

    if len(password) < 8:
        erreurs.append("Le mot de passe doit avoir au moins 8 caractères.")

    if not re.search(r'\d', password):
        erreurs.append("Le mot de passe doit contenir au moins 1 chiffre.")

    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}]', password):
        erreurs.append("Le mot de passe doit contenir au moins 1 caractère spécial.")

    if erreurs:
        raise ValidationError(erreurs)
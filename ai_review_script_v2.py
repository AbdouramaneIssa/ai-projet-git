import os
import sys
import json
from openai import OpenAI

# Configuration de l'API OpenAI (compatible avec l'API Gemini via la variable d'environnement)
try:
    # L'URL de base est définie par l'environnement si l'utilisateur utilise un proxy Gemini
    # Sinon, elle utilise l'API OpenAI par défaut.
    client = OpenAI()
except Exception as e:
    client = None

def generate_html_email(analysis_report):
    """
    Génère le code HTML complet de l'email à partir du rapport d'analyse.
    Le style est amélioré pour être esthétique et professionnel.
    """
    # Le rapport de l'IA est supposé être en Markdown pour une meilleure structuration
    # On le convertit en HTML simple pour l'inclusion dans le corps de l'email
    html_report = analysis_report.replace('\n', '<br>')
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rapport d'Analyse de Code par IA - Impeccable !</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; background-color: #f4f7fa; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 40px auto; background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-top: 5px solid #007bff; }}
        h1 {{ color: #007bff; font-size: 24px; border-bottom: 1px solid #e0e0e0; padding-bottom: 15px; margin-top: 0; }}
        h2 {{ color: #333333; font-size: 18px; margin-top: 25px; }}
        p {{ color: #555555; line-height: 1.6; }}
        .report-section {{ margin-top: 20px; padding: 15px; border-radius: 8px; background-color: #f9f9f9; border: 1px solid #eee; }}
        .impeccable {{ background-color: #e6ffed; border-left: 5px solid #28a745; padding: 15px; margin-bottom: 20px; font-weight: bold; color: #155724; }}
        .error {{ background-color: #f8d7da; border-left: 5px solid #dc3545; padding: 15px; margin-bottom: 20px; font-weight: bold; color: #721c24; }}
        .footer {{ margin-top: 40px; text-align: center; color: #999999; font-size: 12px; border-top: 1px solid #e0e0e0; padding-top: 15px; }}
        code {{ background-color: #eeeeee; padding: 2px 4px; border-radius: 4px; font-size: 90%; }}
        pre {{ background-color: #e9ecef; border: 1px solid #ced4da; padding: 10px; overflow-x: auto; border-radius: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Rapport d'Analyse de Code Automatisée</h1>
        <p>Bonjour,</p>
        <p>Votre dernier push a été analysé par notre système d'Intelligence Artificielle. Voici le rapport détaillé de votre contribution :</p>

        <div class="report-section">
            {html_report}
        </div>

        <p>Nous vous encourageons à consulter les points soulevés pour continuer à améliorer la qualité de votre code.</p>

        <div class="footer">
            Ceci est un email généré automatiquement par Manus AI. Veuillez ne pas y répondre.
        </div>
    </div>
</body>
</html>
"""
    return html_content

def analyze_code_with_ai(code_diff):
    """
    Appelle l'API de l'IA pour obtenir un rapport d'analyse détaillé.
    """
    # Le prompt est ajusté pour répondre aux exigences de l'utilisateur
    system_prompt = (
        "Vous êtes un expert en revue de code rigoureux et encourageant. "
        "Votre tâche est d'analyser le 'diff' de code fourni pour la cohérence, les meilleures pratiques, et les erreurs potentielles. "
        "Formulez votre réponse en utilisant le format Markdown pour une meilleure lisibilité. "
        "Le rapport doit être structuré comme suit :\n\n"
        "1. **Titre et Évaluation Globale** : Commencez par une phrase d'accroche (ex: 'Push Impeccable !' ou 'Attention : Erreurs Détectées').\n"
        "2. **Points Forts** : Mentionnez au moins un point positif.\n"
        "3. **Points à Améliorer/Erreurs** : \n"
        "   - Si des erreurs sont détectées, **mentionnez la ligne ou la fonction concernée** (si possible) et proposez une **suggestion de correction**.\n"
        "   - S'il n'y a pas d'erreur, proposez au moins **deux points d'amélioration** (performance, lisibilité, style).\n"
        "4. **Conclusion** : Un mot d'encouragement final."
    )

    user_prompt = f"Voici le 'diff' du code à analyser:\n\n```diff\n{code_diff}\n```"

    if client:
        try:
            # Utilisation d'un modèle rapide et performant
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Modèle compatible OpenAI
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return (
                f"**Échec de l'Analyse IA**\n\n"
                f"Le système d'IA n'a pas pu traiter votre requête (Erreur: {e}). "
                "Veuillez vérifier la configuration de la clé API ou réessayer plus tard."
            )
    else:
        return (
            "**Rapport d'Analyse Simulé**\n\n"
            "**Titre et Évaluation Globale** : Push Impeccable ! 🎉\n\n"
            "**Points Forts:**\n"
            "* Excellente gestion des dépendances dans le fichier `package.json`.\n\n"
            "**Points à Améliorer:**\n"
            "1. **Lisibilité:** L'indentation de la fonction `calculate_sum` (lignes 15-20) pourrait être simplifiée pour une meilleure lisibilité.\n"
            "2. **Performance:** L'utilisation de boucles imbriquées dans `process_data` pourrait être coûteuse en temps. Considérez une approche par dictionnaire pour optimiser.\n\n"
            "**Conclusion:**\n"
            "Très bon travail ! Continuez sur cette lancée pour maintenir un code de haute qualité."
        )


def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    diff_file_path = sys.argv[1]
    output_html_path = sys.argv[2]

    # 1. Lire le diff du code
    try:
        with open(diff_file_path, 'r') as f:
            code_diff = f.read()
    except FileNotFoundError:
        sys.exit(1)

    # 2. Analyser avec l'IA
    analysis_report = analyze_code_with_ai(code_diff)

    # 3. Générer l'email HTML
    html_email_content = generate_html_email(analysis_report)

    # 4. Sauvegarder l'email HTML dans un fichier de sortie
    try:
        with open(output_html_path, 'w') as f:
            f.write(html_email_content)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()


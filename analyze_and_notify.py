"""
Script Python exécuté automatiquement par GitHub Actions.
Objectif :
- Vérifier le typage du code avec Mypy.
- Envoyer un e-mail automatique avec un résumé généré par Gemini.
- Retourner un code d’échec (1) si Mypy échoue → cela bloque le workflow CI.
"""

import os
import sys
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai

# --- 🔐 Récupération des secrets définis dans GitHub Actions ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

# --- 📩 Vérification des arguments ---
if len(sys.argv) < 3:
    print("Erreur: L'email du destinataire et la liste des fichiers modifiés sont requis.")
    sys.exit(1)

RECIPIENT_EMAIL = sys.argv[1]
CHANGED_FILES = sys.argv[2].split()

# --- 📂 Lecture sécurisée de fichiers ---
def get_file_content(file_path: str) -> str:
    """Lit les 100 premières lignes d'un fichier pour l'analyse."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = "".join(f.readlines()[:100])
        return f"--- Contenu du fichier: {file_path} ---\n{content}\n"
    except Exception as e:
        return f"--- Impossible de lire {file_path} (Erreur: {e}) ---\n"

# --- 🧠 Vérification du typage Mypy ---
def run_mypy_verification():
    """Exécute Mypy et renvoie (succès, rapport)."""
    print("🚀 Lancement de la vérification Mypy...")
    try:
        result = subprocess.run(
            ['mypy', '.', '--ignore-missing-imports'],
            capture_output=True,
            text=True,
            check=False
        )
        success = result.returncode == 0
        report = result.stdout
        print(f"✅ Vérification terminée. Succès: {success}")
        return success, report
    except Exception as e:
        return False, f"Erreur lors de l'exécution de Mypy: {e}"

# --- 💬 Préparation du prompt IA ---
def generate_prompt(changed_files, mypy_report):
    """Construit le prompt pour Gemini, avec le rapport Mypy."""
    mypy_section = (
        "--- Rapport de Vérification Mypy ---\n"
        f"{mypy_report}\n"
        "------------------------------------\n\n"
    )
    prompt = (
        "Vous êtes un expert en typage Python. "
        "Analysez les fichiers suivants et les erreurs Mypy. "
        "Expliquez clairement au développeur comment corriger les erreurs "
        "et rédigez un rapport HTML esthétique et professionnel.\n\n"
        f"{mypy_section}"
    )
    for file in changed_files:
        if file.startswith('.github/') or not file.endswith('.py'):
            continue
        prompt += get_file_content(file)
    return prompt

# --- 🤖 Appel de l'API Gemini ---
def get_ai_review(prompt: str) -> str:
    """Génère le rapport HTML à partir de Gemini."""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        html = response.text.strip()
        if html.startswith("```html"):
            html = html.strip("```html").strip("```").strip()
        return html
    except Exception as e:
        return f"<h1>Erreur Gemini</h1><p>{e}</p>"

# --- 📧 Envoi d'email ---
def send_email(recipient, subject, html_body):
    """Envoie un email HTML via SMTP (Gmail)."""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.close()
        print(f"📨 Email envoyé à {recipient}")
    except Exception as e:
        print(f"⚠️ Échec de l'envoi d'email: {e}")
        print(html_body)

# --- 🚦 Logique principale ---
print(f"Analyse du push pour {RECIPIENT_EMAIL}")
print(f"Fichiers modifiés : {', '.join(CHANGED_FILES)}")

mypy_success, mypy_report = run_mypy_verification()
review_prompt = generate_prompt(CHANGED_FILES, mypy_report)
html_review = get_ai_review(review_prompt)

subject = "✅ Vérification Mypy réussie" if mypy_success else "❌ Échec Mypy - Typage à corriger"
send_email(RECIPIENT_EMAIL, subject, html_review)

# --- 🧱 Code de sortie ---
if not mypy_success:
    print("❌ Erreurs détectées, le workflow va échouer.")
    print(mypy_report)
    sys.exit(1)  # ⚠️ IMPORTANT : ceci fait échouer le workflow GitHub Actions
else:
    print("✅ Tout est conforme. Fin du script.")
    sys.exit(0)  # Le workflow passe

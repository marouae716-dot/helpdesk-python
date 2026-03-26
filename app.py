#Ce code est le point d'entrée principal d'une application web Flask 
#qui gère un système HelpDesk (gestion de tickets de support). 
#Il fait le lien entre l'interface HTML et le code python

from flask import Flask, render_template, request, redirect, url_for

# les outils Flask utilisées :
# Flask : classe principale pour créer l'application web
# render_template : permet d'afficher des fichiers HTML (templates)
# request : permet de lire les données envoyées par HTML
# redirect : redirige l'utilisateur vers autre page
# url_for : génère automatiquement l'URL d'une fonction de route 

from projet import HelpDesk

# Importation de la classe HelpDesk depuis le fichier projet.py

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__)
helpdesk = HelpDesk()

# Création de l'application Flask avec un dossier de templates personnalisé

# ROUTE PRINCIPALE (page d'accueil)
@app.route("/") 
# Définit que cette fonction répond aux requêtes GET sur "/"
def index():
    tickets = helpdesk.get_all_tickets()
    # Récupère la liste de tous les tickets actifs
    file_attente = helpdesk.get_file()
    # Récupère les tickets en attente de traitement
    historique = helpdesk.get_historique()
    # Récupère l'historique des tickets résolus
    nb_tickets, nb_file, nb_hist = helpdesk.statistiques()
    # Récupère les statistiques

    # Affiche la page HTML "index.html" en lui passant toutes les données nécessaires
    return render_template(
        "index.html",
        tickets=tickets,
        file_attente=file_attente,
        historique=historique,
        nb_tickets=nb_tickets,
        nb_file=nb_file,
        nb_hist=nb_hist
    )

#ROUTE : CRÉER UN NOUVEAU TICKET
@app.route("/creer_ticket", methods=["POST"])
def creer_ticket():
    client = request.form.get("client")
    description = request.form.get("description")
    priorite = request.form.get("priorite")
    categorie = request.form.get("categorie")

    # Vérifie que tous les champs sont remplis avant de créer le ticket
    if client and description and priorite and categorie:
        helpdesk.creer_ticket(client, description, priorite, categorie)

    # Redirige vers la page d'accueil après création
    return redirect(url_for("index"))

# ROUTE : SUPPRIMER UN TICKET
@app.route("/supprimer_ticket", methods=["POST"])
def supprimer_ticket():
    ticket_id = request.form.get("ticket_id")
    if ticket_id:
        try:
            ticket_id = int(ticket_id)
            helpdesk.supprimer_ticket(ticket_id)
        except ValueError:
            pass
    return redirect(url_for("index"))

#ROUTE : TRAITER LE PROCHAIN TICKET EN FILE D'ATTENTE
@app.route("/traiter_ticket", methods=["POST"])
def traiter_ticket():
    helpdesk.traiter_ticket()
    return redirect(url_for("index"))

#ROUTE : MARQUER UN TICKET COMME RÉSOLU
@app.route("/resoudre_ticket", methods=["POST"])
def resoudre_ticket():
    ticket_id = request.form.get("ticket_resolu_id")
    if ticket_id:
        try:
            ticket_id = int(ticket_id)
            helpdesk.resoudre_ticket(ticket_id)
        except ValueError:
            pass
    return redirect(url_for("index"))

#ROUTE : VIDER L'HISTORIQUE DES TICKETS RÉSOLUS
@app.route("/vider_historique", methods=["POST"])
def vider_historique():
    helpdesk.vider_historique()
    return redirect(url_for("index"))


# Lance le serveur Flask uniquement si ce fichier est exécuté directement (pas importé)
# debug=True : active le rechargement automatique et l'affichage des erreurs dans le navigateur
if __name__ == "__main__":
    app.run(debug=True)
    
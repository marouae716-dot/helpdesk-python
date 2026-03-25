from flask import Flask, render_template, request, redirect, url_for
from projet import HelpDesk
import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__)
helpdesk = HelpDesk()


@app.route("/")
def index():
    tickets = helpdesk.get_all_tickets()
    file_attente = helpdesk.get_file()
    historique = helpdesk.get_historique()
    nb_tickets, nb_file, nb_hist = helpdesk.statistiques()
    return render_template(
        "index.html",
        tickets=tickets,
        file_attente=file_attente,
        historique=historique,
        nb_tickets=nb_tickets,
        nb_file=nb_file,
        nb_hist=nb_hist
    )


@app.route("/creer_ticket", methods=["POST"])
def creer_ticket():
    client = request.form.get("client")
    description = request.form.get("description")
    priorite = request.form.get("priorite")
    categorie = request.form.get("categorie")
    if client and description and priorite and categorie:
        helpdesk.creer_ticket(client, description, priorite, categorie)
    return redirect(url_for("index"))


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


@app.route("/traiter_ticket", methods=["POST"])
def traiter_ticket():
    helpdesk.traiter_ticket()
    return redirect(url_for("index"))


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


@app.route("/vider_historique", methods=["POST"])
def vider_historique():
    helpdesk.vider_historique()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)


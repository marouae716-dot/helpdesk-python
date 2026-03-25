# code python pour le systeme de helpdesk

# Classe représentant un ticket
class Ticket:
    # Initialisation des attributs d'un ticket
    def __init__(self, ticket_id, client, description, priorite, categorie, status="Ouvert"):
        self.id = ticket_id  # ID unique du ticket
        self.client = client  # Nom du client
        self.description = description  # Description du problème
        self.priorite = priorite  # Priorité du ticket (faible, moyenne, urgente)
        self.categorie = categorie  # Catégorie du problème
        self.status = status  # Statut du ticket (Ouvert, En cours, Résolu)
        self.next = None  # Pointeur vers le prochain ticket dans la liste chaînée

    # Méthode pour afficher les détails du ticket
    def afficher_ticket(self):
        return f"[{self.id}] {self.client} - {self.priorite} - {self.categorie} - {self.status} - {self.description}"


# Classe représentant une liste liée de tickets
class ListeTickets :
    # Initialisation de la liste chaînée
    def __init__(self):
        self.tete = None  # Tête de la liste, initialement vide

    # Méthode pour ajouter un ticket à la liste
    def ajouter_ticket(self, ticket):
        if self.tete is None:  # Si la liste est vide
            self.tete = ticket  # Le nouveau ticket devient la tête
        else:
            courant = self.tete  # Commencer à la tête de la liste
            while courant.next is not None:  # Parcourir jusqu'au dernier ticket
                courant = courant.next
            courant.next = ticket  # Ajouter le nouveau ticket à la fin

    # Méthode pour supprimer un ticket par son ID
    def supprimer_ticket(self, ticket_id):
        courant = self.tete  # Commencer à la tête de la liste
        precedent = None  # Pour garder une trace du ticket précédent
        while courant is not None and courant.id != ticket_id:  # Chercher le ticket
            precedent = courant  # Mettre à jour le précédent
            courant = courant.next  # Passer au suivant
        if courant is None:  # Si le ticket n'a pas été trouvé
            return False  # Retourner False
        if precedent is None:  # Si le ticket à supprimer est la tête
            self.tete = courant.next  # Mettre à jour la tête
        else:
            precedent.next = courant.next  # Déconnecter le ticket à supprimer
        return True  # Retourner True si la suppression a réussi
    
    # Méthode pour trouver un ticket par son ID
    def trouver_ticket(self, ticket_id):
        courant = self.tete  # Commencer à la tête de la liste
        while courant is not None:  # Parcourir la liste
            if courant.id == ticket_id:  # Si le ticket est trouvé
                return courant  # Retourner le ticket
            courant = courant.next  # Passer au suivant
        return None  # Retourner None si le ticket n'est pas trouvé
    
    # Méthode pour afficher tous les tickets dans la liste
    def afficher_tickets(self):
        tickets = []  # Liste pour stocker les tickets à afficher
        courant = self.tete  # Commencer à la tête de la liste
        while courant is not None:  # Parcourir la liste
            tickets.append(courant.afficher_ticket())  # Ajouter chaque ticket à la liste
            courant = courant.next  # Passer au suivant
        return tickets  # Retourner la liste des tickets

#_________________________________    
# Classe représentant une file d'attente
# On utilise file pour que le premier ticket créé soit le premier traité (FIFO)
class FileTickets:
    # Initialisation de la file
    def __init__(self):
        self.front = None  # Front de la file, initialement vide
        self.rear = None   # Rear de la file, initialement vide

    # Méthode pour ajouter un ticket à la file
    def enfiler(self, ticket):
        if self.rear is None:  # Si la file est vide
            self.front = self.rear = ticket  # Le nouveau ticket devient front et rear
        else:
            self.rear.next = ticket  # Ajouter le ticket à la fin de la file
            self.rear = ticket  # Mettre à jour le rear

    # Méthode pour retirer un ticket de la file
    def defiler(self):
        if self.front is None:  # Si la file est vide
            return None  # Retourner None
        ticket = self.front  # Prendre le ticket en tête
        self.front = self.front.next  # Mettre à jour le front
        if self.front is None:  # Si la file devient vide
            self.rear = None  # Mettre à jour le rear
        ticket.next = None  # Déconnecter le ticket
        return ticket  # Retourner le ticket traité
    
    # Méthode pour afficher les tickets dans la file
    def afficher_file(self):
        tickets = []  # Liste pour stocker les tickets à afficher
        courant = self.front  # Commencer à l'avant de la file
        while courant is not None:  # Parcourir la file
            tickets.append(courant.afficher_ticket())  # Ajouter chaque ticket à la liste
            courant = courant.next  # Passer au suivant
        return tickets  # Retourner la liste des tickets

#_________________________________    
#historique des actions
#on utilise une pile pour que le dernier ticket triate soit le premier à etre affiché (LIFO)
class Historique:
    # Initialisation de la pile
    def __init__(self):
        self.pile = []  # Liste pour stocker les actions

    # Méthode pour enregistrer une action
    def push(self, action):
        self.pile.append(action)  # Ajouter l'action à la pile (push = ajputer )

    # Méthode pour annuler la dernière action
    def pop(self):
        if not self.pile:  # Si la pile est vide
            return None  # Retourner None
        return self.pile.pop()  # Retourner la dernière action (pop = retirer avec retourner)
    
    # Méthode pour afficher l'historique des actions
    def afficher_historique(self):
        return self.pile.copy()  # Retourner la pile

    # Méthode pour vider complètement l'historique
    def vider(self):
        self.pile = []  # Réinitialiser la pile à une liste vide


#_________________________________   
# Class principale pour le systeme 
class HelpDesk:
    # Initialisation du Help Desk
    def __init__(self):
        self.liste_tickets = ListeTickets()  # Créer une nouvelle liste de tickets
        self.file_tickets = FileTickets()  # Créer une nouvelle file de tickets
        self.historique = Historique()  # Créer un nouvel historique
        self.compteur_id = 1  # Compteur pour générer des IDs uniques

    # Méthode pour créer un nouveau ticket
    def creer_ticket(self, client, description, priorite, categorie):
        ticket = Ticket(self.compteur_id, client, description, priorite, categorie)  # Créer un nouveau ticket
        self.compteur_id += 1  # Incrémenter l'ID pour le prochain ticket
        self.liste_tickets.ajouter_ticket(ticket)  # Ajouter le ticket à la liste
        self.file_tickets.enfiler(ticket)  # Ajouter le ticket à la file
        self.historique.push(f"Création ticket {ticket.afficher_ticket()}")  # Enregistrer l'action dans l'historique
        return ticket  # Retourner le ticket créé
    
    # Méthode pour traiter le premier ticket dans la file
    def traiter_ticket(self):
        ticket = self.file_tickets.defiler()  # Retirer le ticket de la file
        if ticket is None:  # Si aucun ticket à traiter
            return None  # Retourner None
        ticket.status = "En cours"  # Mettre à jour le statut du ticket
        self.historique.push(f"Traitement ticket {ticket.afficher_ticket()}")  # Enregistrer l'action dans l'historique
        return ticket  # Retourner le ticket traité
    
    # Méthode pour résoudre un ticket
    def resoudre_ticket(self, ticket_id):
        ticket = self.liste_tickets.trouver_ticket(ticket_id)  # Trouver le ticket par ID
        if ticket is None:  # Si le ticket n'existe pas
            return False  # Retourner False
        ticket.status = "Résolu"  # Mettre à jour le statut
        self.historique.push(f"Résolution ticket {ticket.afficher_ticket()}")  # Enregistrer l'action dans l'historique
        return True  # Retourner True si la résolution a réussi
    
    # Méthode pour supprimer un ticket utilisant son ID
    def supprimer_ticket(self, ticket_id):
        ticket = self.liste_tickets.trouver_ticket(ticket_id)  # Trouver le ticket
        if ticket is None:  # Si le ticket n'existe pas
            return False  # Retourner False
        self.liste_tickets.supprimer_ticket(ticket_id)  # Supprimer le ticket de la liste
        self.historique.push(f"Suppression ticket ID={ticket_id}")  # Enregistrer l'action dans l'historique
        return True  # Retourner True si la suppression a réussi
    
    # Méthode pour obtenir tous les tickets existants
    def get_all_tickets(self):
        return self.liste_tickets.afficher_tickets()  # Retourner tous les tickets de la liste
    
    # Méthode pour obtenir les tickets en attente de resolution dans la file
    def get_file(self):
        return self.file_tickets.afficher_file()  # Retourner la file de tickets
    
    # Méthode pour obtenir l'historique des actions
    def get_historique(self):
        return self.historique.afficher_historique()  # Retourner l'historique des actions
    
    # Méthode pour vider l'historique des action
    def vider_historique(self):
        self.historique.vider()  # Appeler la méthode vider de l'historique
    
    # Méthode pour obtenir des statistiques sur le système
    def statistiques(self):
        nb_tickets = len(self.liste_tickets.afficher_tickets())  # Compter le nombre de tickets
        nb_file = len(self.file_tickets.afficher_file())  # Compter le nombre de tickets en file
        nb_hist = len(self.historique.afficher_historique())  # Compter le nombre d'actions enregistrées
        return nb_tickets, nb_file, nb_hist  # Retourner les statistiques

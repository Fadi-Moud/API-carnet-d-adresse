import os
from pymongo import MongoClient


class ContactInterface:
    def __init__(self):
        # Établir la connexion à MongoDB
        self.client = MongoClient(os.getenv('DATABASE_URL', None))

        # Accéder à la base de données
        self.db = self.client["contacts+"]

        # Accéder à la collection des contacts
        self.contacts = self.db["contacts"]

    def create_contact(self, data):
        """
            Crée un nouveau contact dans la collection.

            Paramètre :
                - data : un dictionnaire représentant les données du                 nouveau contact.

            Retour :
                - Le résultat de l'opération de création.
        """
        self.contacts.insert_one(data)
        data['_id'] = str(data['_id'])
        return data

    def update_contact(self, filter, updated_contact):
        """
            Met à jour un contact existant dans la collection.

            Paramètres :
                - filter : un dictionnaire représentant le filtre pour trouver le contact à mettre à jour.
                - updated_contact : un dictionnaire représentant les nouvelles données du contact.

            Retour :
                - Le résultat de l'opération de mise à jour.
        """
        result = self.contacts.update_one(filter, {"$set": updated_contact})
        return result
    
    def delete_contact_params(self, filter):
        """
            Supprime un contact de la collection en fonction du filtre spécifié.

            Paramètre :
                - filter : un dictionnaire représentant le filtre pour trouver le contact à supprimer.

            Retour :
                - Le résultat de l'opération de suppression.
        """
        result = self.contacts.delete_many(filter)
        return result
    
    def delete_contact(self, filter):
        """
            Supprime un contact de la collection en fonction du filtre spécifié.

            Paramètre :
                - filter : un dictionnaire représentant le filtre pour trouver le contact à supprimer.

            Retour :
                - Le résultat de l'opération de suppression.
        """
        result = self.contacts.delete_one(filter)
        return result

    def get_all_contacts(self):
        """
            Récupère tous les contacts de la collection.

            Retour :
                - Une liste contenant tous les contacts.
        """
        # Récupère tous les contacts de la collection
        contacts = list(self.contacts.find())

        # Itère à travers chaque contact récupéré
        for contact in contacts:
            # Convertit l'ObjectId en une chaîne de caractères pour eviter certaines erreur lors du renvoie de réponse
            contact['_id'] = str(contact['_id'])

        # Retourne la liste des contacts modifiée
        return contacts


    def get_contact_by_id(self, filter):
        """
            Récupère un contact par son ID.

            Paramètres :
                - filter : le filtre pour identifier le contact.

            Retour :
                - Le contact correspondant à l'ID spécifié.
        """
        contact = self.contacts.find_one(filter)
        contact['_id'] = str(contact['_id'])
        return contact

# Les modules dont ont nous auront besoin...
from flask import Blueprint, request, jsonify
from bson import ObjectId

# ContactInterface étant l'interface qui nous permettra de gérer notre
# collection de contacts que nous allons définir dans interface.py
from .interface import ContactInterface

contact_request = Blueprint('contacts', __name__)


@contact_request.route('/create', methods=['POST'])
def create_contact():
    """
    Route pour créer un nouveau contact
    Méthode : POST
    """
    # Obtenir les données du contact à partir de la requête
    data = request.get_json()

    # Utilisation de l'interface pour créer un nouveau contact
    new_contact = ContactInterface().create_contact(data)

    # Renvoyer le nouveau contact créé sous forme de réponse JSON ou un texte
    # en cas d'erreur
    if not data:
        return jsonify(message="Erreur de création. Réessayer"), 400
    return jsonify(new_contact), 201
    # Implémentation pour créer un nouveau contact


@contact_request.route('/update', methods=['PUT'])
def update_contact():
    """
    Route pour mettre à jour un contact existant
    Méthode : PUT
    """
    data = request.get_json()

    if not data:
        return jsonify(message="Données de contact manquantes"), 400
    contact_id = data.get('id')

    if not contact_id:
        return jsonify(message="ID de contact manquant"), 400

    updated_contact = {}

    if 'surname' in data:
        updated_contact['surname'] = data.get('surname')

    if 'lastname' in data:
        updated_contact['lastname'] = data.get('lastname')

    if 'email' in data:
        updated_contact['email'] = data.get('email')

    if 'phone' in data:
        updated_contact['phone'] = data.get('phone')

    filter = {'_id': ObjectId(contact_id)}
    result = ContactInterface().update_contact(filter, updated_contact)

    if not result:
        return jsonify(message="Contact non trouvé"), 404

    return jsonify(message="Contact mis à jour avec succès"), 200

    # Implémentation pour mettre à jour un contact existant


@contact_request.route('/delete', methods=['DELETE'])
def delete_contact():
    """
    Route pour supprimer un contact
    Méthode : DELETE
    """
    data = request.get_json()

    if not data:
        return jsonify(message="Données de contact manquantes"), 400

    contact_id = data.get('id')

    if not contact_id:
        return jsonify(message="ID de contact manquant"), 400

    filter = {'_id': ObjectId(contact_id)}
    result = ContactInterface().delete_contact(filter)

    if not result:
        return jsonify(message="Contact non trouvé"), 404

    return jsonify(message="Contact supprimé avec succès"), 200


@contact_request.route('/delete/params', methods=['DELETE'])
def delete_contact_params():
    """
    Route pour supprimer un contact suivant les paramètres
    Méthode : DELETE
    """
    data = request.get_json()

    if not data:
        return jsonify(message="Données de contact manquantes"), 400

    #Code pour supprimer avec surname
    contact_surname = data.get('surname')
    if 'surname' in data:
        filter = {'surname': contact_surname}
        result = ContactInterface().delete_contact_params(filter)
    

    #Code pour supprimer avec lastname
    contact_lastname = data.get('lastname')
    if 'lastname' in data:
        contact_lastname = data.get('lastname')
        filter = {'lastname':contact_lastname}
        result = ContactInterface().delete_contact_params(filter)
    
    #Code pour supprimer avec email
    contact_email = data.get('email')

    if 'email' in data:
        contact_email = data.get('email')
        filter = {'email':contact_email}
        result = ContactInterface().delete_contact_params(filter)
    
    #Code pour supprimer avec phone
    contact_phone = data.get('phone')
    if 'phone' in data:
        contact_phone = data.get('phone')
        filter = {'phone':contact_phone}
        result = ContactInterface().delete_contact_params(filter)
    
    if not result:
        return jsonify(message="Contact non trouvé"), 404
    
    return jsonify(message="Contact supprimé avec succès"), 200

@contact_request.route('/', methods=['GET'])
def get_all_contacts():
    """
    Route pour récupérer tous les contacts
    Méthode : GET
    """
    contacts = ContactInterface().get_all_contacts()

    if not contacts:
        return jsonify(message="Aucun contact trouvé"), 404

    return jsonify(contacts), 200


@contact_request.route('/<id>', methods=['GET'])
def get_contact_by_id(id):
    """
    Route pour récupérer un contact par son ID
    Méthode : GET
    """
    # Implémentation pour renvoyer un contact spécifique en fonction de son ID
    filter = {'_id': ObjectId(id)}
    contact = ContactInterface().get_contact_by_id(filter)
    if contact:
        return jsonify(contact), 200
    else:
        return jsonify({"message": "Contact not found"}), 404

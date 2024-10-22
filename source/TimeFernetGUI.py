import logging
import base64
import time

from FernetGUI import FernetGUI
from cryptography.fernet import Fernet, InvalidToken

# Durée de vie des messages en secondes (TTL)
DUREE_VIE = 30


class TimeFernetGUI(FernetGUI):
    """
    Classe dérivée de FernetGUI qui utilise un TTL pour la validité des messages.
    """

    # Fonction encrypt avec gestion du TTL
    def encrypt(self, message) -> bytes:
        # Création d'un objet Fernet en utilisant la clé dérivée
        fernet_obj = Fernet(self._key)
        # Obtenir le temps actuel actuelle en secondes
        current_time = int(time.time())
        # Conversion du message en bytes avant chiffrement 
        message_bytes = bytes(message, 'utf-8')
        # Chiffrement du message avec un TTL de 30 secondes à partir du temps actuel
        message_chiffre = fernet_obj.encrypt_at_time(message_bytes, current_time)
        return message_chiffre  # Retourne le message chiffré

    # Fonction decrypt avec gestion du TTL et capture des exceptions
    def decrypt(self, message) -> str:
        # Décodage du message chiffré reçu (encodé en base64)
        message_decode = base64.b64decode(message['data'])
        # Création d'un objet Fernet avec la clé derivée pour le déchiffrement
        fernet_obj = Fernet(self._key)
        # Obtenir le temps actuel en secondes
        current_time = int(time.time())
        try:
            # dechiffrer le message en verifiant qu'il est encore valide selon le TTL de 30 secondes 
            message_dechiffre = fernet_obj.decrypt_at_time(message_decode, DUREE_VIE, current_time).decode('utf8')
            return message_dechiffre  # Retourne le message déchiffré
        except InvalidToken:
            # Gestion de l'exception si le message a expiré ou si la clé est invalide
            error_message = "Erreur : Le message a expiré ou la clé est incorrecte."
            self._log.error(error_message)
            return error_message  # Retourne le message d'erreur en cas d'exception 

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # Instancier la classe TimeFernetGUI
    client = TimeFernetGUI()
    client.create()
    client.loop()

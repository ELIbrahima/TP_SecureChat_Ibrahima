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
        # Création de l'instance Fernet avec la clé dérivée
        fernet_obj = Fernet(self._key)
        # Obtenir l'heure actuelle en secondes
        current_time = int(time.time())
        # Conversion du message en bytes
        message_bytes = bytes(message, 'utf-8')
        # Chiffrement du message avec un TTL de 30 secondes à partir du moment actuel
        message_chiffre = fernet_obj.encrypt_at_time(message_bytes, current_time)
        return message_chiffre  # Retourne le message chiffré

    # Fonction decrypt avec gestion du TTL et gestion des exceptions
    def decrypt(self, message) -> str:
        # Décodage du message chiffré en base64
        message_decode = base64.b64decode(message['data'])
        # Création de l'instance Fernet pour le déchiffrement
        fernet_obj = Fernet(self._key)
        # Obtenir l'heure actuelle en secondes
        current_time = int(time.time())
        try:
            # Tentative de déchiffrement avec vérification du TTL
            message_dechiffre = fernet_obj.decrypt_at_time(message_decode, DUREE_VIE, current_time).decode('utf8')
            return message_dechiffre  # Retourne le message déchiffré
        except InvalidToken:
            # Gestion de l'exception si le message a expiré ou si la clé est invalide
            error_message = "Erreur : Le message a expiré ou la clé est incorrecte."
            self._log.error(error_message)
            return error_message  # Retourne le message d'erreur

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # Instanciation et démarrage du chat avec TimeFernetGUI
    client = TimeFernetGUI()
    client.create()
    client.loop()

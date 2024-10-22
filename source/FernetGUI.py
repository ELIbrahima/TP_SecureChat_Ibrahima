import logging
import base64
import hashlib

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback
from CipheredGUI import CipheredGUI  # Import de la classe CipheredGUI

# Importation de Fernet pour l'authenticated encryption
from cryptography.fernet import Fernet

class FernetGUI(CipheredGUI):  # Dérive de CipheredGUI 

    # Fonction pour demarrer la session de chat avec derivation de la clé Fernet 
    def run_chat(self, sender, app_data) -> None:
        # Recuperation des informations de connexion saisies par l'utilisateur 
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        # Dérivation de la clé à partir du mot de passe en utilisant sha-256 et encoder en base64
        key_bytes = hashlib.sha256(password.encode()).digest()
        key = base64.urlsafe_b64encode(key_bytes[:32])  # utiliser les 32 premiers
        self._key = key # stocker la clé derivée

        # Initialisation du client de chat et enregistrement du nom 
        self._callback = GenericCallback()
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)
        
        # basculer vers l'interface de chat apres la connexion 
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")


    # Fonction pour chiffrer un message avec Fernet 
    def encrypt(self, message) -> bytes:
        # Créer un objet Fernet avec la clé derivée
        fernet = Fernet(self._key)
        # Chiffrer le message 
        encrypted_message = fernet.encrypt(message.encode("utf-8"))
        return encrypted_message # retourner le message chiffré 


    # Fonction pour dechiffrer un message avec Fernet 
    def decrypt(self, message_data) -> str:
        # Déchiffrer le message en base64 reçu
        encrypted_message = base64.b64decode(message_data['data'])
        fernet = Fernet(self._key)
        #  dechiffrer et convertir le message en chaine utf-8
        decrypted_message = fernet.decrypt(encrypted_message).decode('utf-8')
        return decrypted_message # retourner message dechiffé


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Instancier la classe FernetGUI, créer le contexte et démarrer la boucle principale
    client = FernetGUI()
    client.create()
    client.loop()

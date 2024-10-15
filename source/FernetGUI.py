import logging
import base64
import hashlib

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback
from CipheredGUI import CipheredGUI  # Import de la classe CipheredGUI

# Importation de Fernet pour l'authenticated encryption
from cryptography.fernet import Fernet

class FernetGUI(CipheredGUI):  # Dérive de CipheredGUI comme demandé

    def run_chat(self, sender, app_data) -> None:
        # Fonction de rappel pour démarrer la session de chat
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        # Dérivation de la clé à partir du mot de passe avec sha256().digest() et base64.b64encode()
        key_bytes = hashlib.sha256(password.encode()).digest()
        key = base64.urlsafe_b64encode(key_bytes[:32])  # On prend les 32 premiers octets et on encode en base64
        self._key = key
        
        self._callback = GenericCallback()
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)
        
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, message) -> bytes:
        # Créer un objet Fernet avec la clé
        fernet = Fernet(self._key)
        # Chiffrer le message
        encrypted_message = fernet.encrypt(message.encode("utf-8"))
        return encrypted_message

    def decrypt(self, message_data) -> str:
        # Déchiffrer le message en base64
        encrypted_message = base64.b64decode(message_data['data'])
        fernet = Fernet(self._key)
        decrypted_message = fernet.decrypt(encrypted_message).decode('utf-8')
        return decrypted_message


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Instancier la classe FernetGUI, créer le contexte et démarrer la boucle principale
    client = FernetGUI()
    client.create()
    client.loop()

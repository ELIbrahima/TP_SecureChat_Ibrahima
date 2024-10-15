import logging
import base64
import os  # Pour la génération de l'IV et d'autres fonctionnalités du système

# Bibliothèque pour l'interface graphique
import dearpygui.dearpygui as dpg

# Importer les classes pour le client de chat et les callbacks
from chat_client import ChatClient
from generic_callback import GenericCallback
from basic_gui import BasicGUI, DEFAULT_VALUES

# Import pour la dérivation de clé et le hachage
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Importer les algorithmes de chiffrement (AES) et les modes de chiffrement
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Variables modifiées par rapport à ton collègue
TAILLE_CLE = 16  # Taille de la clé AES en octets
NB_ITERATIONS = 1500  # Changer le nombre d'itérations pour différencier
SEL_PERSONNALISE = b"mon_sel_unique"  # Sel personnalisé
TAILLE_BLOC_AES = 128  # Taille en bits pour AES

class CipheredGUI(BasicGUI):
    """
    GUI pour un chat client avec chiffrement AES.
    """
    def __init__(self) -> None:
        super().__init__()
        self._key = None

    def _create_connection_window(self) -> None:
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            # Ajouter le champ password selon les consignes du prof
            with dpg.group(horizontal=True):
                dpg.add_text("password")
                dpg.add_input_text(default_value="", tag="connection_password", password=True)
            dpg.add_button(label="Connect", callback=self.run_chat)

    def run_chat(self, sender, app_data) -> None:
        # Récupérer les informations de connexion et le mot de passe
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        # Dérivation de la clé avec PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=TAILLE_CLE,
            salt=SEL_PERSONNALISE,
            iterations=NB_ITERATIONS,
            backend=default_backend()
        )
        self._key = kdf.derive(bytes(password, "utf8"))  # Stockage de la clé

        # Initialiser le client de chat
        self._callback = GenericCallback()
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        # Afficher la fenêtre de chat
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting...")

    # Fonction encrypt selon les consignes du prof
    def encrypt(self, message):
        iv = os.urandom(16)  # Générer un IV aléatoire
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv))
        encryptor = cipher.encryptor()

        # Ajout du padding PKCS7
        padder = padding.PKCS7(TAILLE_BLOC_AES).padder()
        padded_message = padder.update(bytes(message, "utf8")) + padder.finalize()

        # Chiffrement du message
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

        return (iv, encrypted_message)  # Retourner le tuple (iv, message chiffré)

    # Fonction decrypt selon les consignes du prof
    def decrypt(self, encrypted_message):
        iv = base64.b64decode(encrypted_message[0]['data'])
        encrypted_data = base64.b64decode(encrypted_message[1]['data'])

        # Déchiffrement avec AES-CTR
        decryptor = Cipher(algorithms.AES(self._key), modes.CTR(iv), backend=default_backend()).decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Retirer le padding PKCS7
        unpadder = padding.PKCS7(TAILLE_BLOC_AES).unpadder()
        message_dechiffre = unpadder.update(decrypted_data) + unpadder.finalize()

        return message_dechiffre.decode("utf8")  # Retourner le message déchiffré

    def send(self, text) -> None:
        # Fonction pour chiffrer et envoyer le message
        encrypted_message = self.encrypt(text)
        self._client.send_message(encrypted_message)

    def recv(self) -> None:
        # Fonction pour recevoir et déchiffrer les messages
        if self._callback is not None:
            for user, encrypted_message in self._callback.get():
                decrypted_message = self.decrypt(encrypted_message)
                self.update_text_screen(f"{user}: {decrypted_message}")
            self._callback.clear()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = CipheredGUI()
    client.create()
    client.loop()

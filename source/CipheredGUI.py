import logging
import base64
import os  # Pour la génération de l'IV

# Bibliothèque pour l'interface graphique
import dearpygui.dearpygui as dpg

# Importation des classes pour le client de chat et les callbacks
from chat_client import ChatClient
from generic_callback import GenericCallback
from basic_gui import BasicGUI, DEFAULT_VALUES

# Import pour la dérivation de clé et le hachage
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Importation des algorithmes de chiffrement (AES) et les modes de chiffrement
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Configuration pour AES (Taille de la Clé, nombre d'itérations, etc)
TAILLE_CLE = 16  # Taille de la clé AES en octets
NB_ITERATIONS = 1500  # nombre d'itérations pour la dérivation de clé
SEL_PERSONNALISE = b"mon_sel_unique"  # Sel utilisé pour la dérivation de clé
TAILLE_BLOC_AES = 128  # Taille des blocs pour AES en bits

class CipheredGUI(BasicGUI):
    """
    GUI pour un chat client avec chiffrement AES.
    """
    def __init__(self) -> None:
        super().__init__()
        # La clé de chiffrement sera dérivée plus tard à partir du mot de passe
        self._key = None


     # Création de la fenetre de connextion
    def _create_connection_window(self) -> None:
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            # Ajout du champ "password" pour saisir le mot de passe
            with dpg.group(horizontal=True):
                dpg.add_text("password")
                dpg.add_input_text(default_value="", tag="connection_password", password=True)
            dpg.add_button(label="Connect", callback=self.run_chat)

     # Gestion de la connexion et de la dérivation de clé à partir du mot de passe
    def run_chat(self, sender, app_data) -> None:
        # Récupération des informations de connexion
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        # Dérivation de la clé avec PBKDF2 à partir du mot de passe et du sel 
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=TAILLE_CLE,
            salt=SEL_PERSONNALISE,
            iterations=NB_ITERATIONS,
            backend=default_backend()
        )
        self._key = kdf.derive(bytes(password, "utf8"))  # clé derivé du mot de passe

        # Initialisation du client de chat
        self._callback = GenericCallback()
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        # Affichage de la fenêtre de chat aprés connexion
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting...")

    # Fonction encrypt pour chiffrer les messages avant l'envoi
    def encrypt(self, message):
        iv = os.urandom(16)  # Générer un IV aléatoire pour chaque message
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv)) # Chiffrement AES en mode CTR
        encryptor = cipher.encryptor()

        # Ajout d'un padding PKCS7 pour s'assurer que le message soit de la bonne taille
        padder = padding.PKCS7(TAILLE_BLOC_AES).padder()
        padded_message = padder.update(bytes(message, "utf8")) + padder.finalize()

        # Chiffrement du message
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

        return (iv, encrypted_message)  # Retourner l'iv et le message chiffré

    # Fonction decrypt pour dechiffrer les messages 
    def decrypt(self, encrypted_message):
        #extraire l'IV et les données chiffrées
        iv = base64.b64decode(encrypted_message[0]['data'])
        encrypted_data = base64.b64decode(encrypted_message[1]['data'])

        # Déchiffrement avec AES en mode CTR
        decryptor = Cipher(algorithms.AES(self._key), modes.CTR(iv), backend=default_backend()).decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Retirer le padding PKCS7 ajouté lors du chiffrement 
        unpadder = padding.PKCS7(TAILLE_BLOC_AES).unpadder()
        message_dechiffre = unpadder.update(decrypted_data) + unpadder.finalize()

        return message_dechiffre.decode("utf8")  # Retourner le message déchiffré en UTF-8

    # Fonction d'envoi des messages chiffrés
    def send(self, text) -> None:
        # Chiffrer le message avant l'envoi 
        encrypted_message = self.encrypt(text)
        # Envoi le message chiffré au serveur 
        self._client.send_message(encrypted_message)

    # Fonction de récéption et de déchiffrement des messages 
    def recv(self) -> None:
        # Verifier s'il y a des messages à recevoir 
        if self._callback is not None:
            for user, encrypted_message in self._callback.get():
                # dechiffrer le message reçu 
                decrypted_message = self.decrypt(encrypted_message)
                # afficher le message dans l'interface 
                self.update_text_screen(f"{user}: {decrypted_message}")
            self._callback.clear()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = CipheredGUI()
    client.create()
    client.loop()

# Prise en Main 

1) C'est une architecture client-serveur où deux clients sont connectés simultanément au meme serveur pour échanger des messages.

2) Les logs affichent les différentes actions des clients et du serveur, y compris la connexion des utilisateurs et l'échange des messages entre eux, ce qui permet de suivre ce qui se passe en temps réel.

3) L'absence de chiffrement des messages est un probléme, car n'importe qui sur le réseau peut intercepter et lire ces messages. Cela va à l'encontre du principe de securité selon lequel la confidentialité des données doit etre garantie.

4) La solution serait d'utiliser un chiffrement symétrique comme AES pour proteger les messages. Le message serait chiffré avec une clé secrété partagée, et seul le destinataire connaissant cette clé pourrait déchiffrer le message.

# Chiffrement 
# Prise en Main 

1) C'est une architecture client-serveur où deux clients sont connectés simultanément au meme serveur pour échanger des messages.

2) Les logs affichent les différentes actions des clients et du serveur, y compris la connexion des utilisateurs et l'échange des messages entre eux, ce qui permet de suivre ce qui se passe en temps réel.

3) L'absence de chiffrement des messages est un probléme, car n'importe qui sur le réseau peut intercepter et lire ces messages. Cela va à l'encontre du principe de securité selon lequel la confidentialité des données doit etre garantie.

4) La solution serait d'utiliser un chiffrement symétrique comme AES pour proteger les messages. Le message serait chiffré avec une clé secrété partagée, et seul le destinataire connaissant cette clé pourrait déchiffrer le message.

# Chiffrement 

1) urandom est généralement utilisé pour générer des nombres aléatoires, mais pour la cryptographie, il peut ne pas être idéal dans certains cas. Il manque parfois de sécurité maximale pour des usages très sensibles, car il pourrait être prévisible dans certaines situations spécifiques. Il vaut mieux utiliser des générateurs de nombres aléatoires vraiment sécurisés, comme ceux fournis par les bibliothèques cryptographiques.

2) Utiliser des primitives cryptographiques peut être risqué si on ne comprend pas leur fonctionnement en profondeur. Une petite erreur dans l'implémentation peut entraîner des failles importantes, rendant le système vulnérable. Par exemple, mal gérer les clés ou ne pas bien utiliser le padding peut compromettre la sécurité.

3) Le chiffrement ne protège que les données elles-mêmes, pas la manière dont elles sont utilisées. Un serveur malveillant peut toujours manipuler ou altérer les données chiffrées, envoyer de fausses informations, ou même bloquer le service. Le chiffrement n’empêche pas ce type d’attaques.

4) Ce qui manque, c'est l'authentification. Le chiffrement protège les données, mais sans une vérification d'authenticité (comme un HMAC), il est impossible de garantir que le message n'a pas été modifié ou qu'il provient de la bonne source.


# Authenticated Symetric Encryption
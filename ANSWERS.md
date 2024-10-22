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

1) Fernet est plus sûr car il est conçu pour gérer à la fois le chiffrement et la vérification d'intégrité automatiquement, sans que l'on ait à s'en préoccuper. Cela réduit le risque d'erreurs dans l'implémentation, notamment en ce qui concerne le padding et l'intégrité des données.

2) On appelle cela une attaque par relecture ou replay attack, où un attaquant envoie de nouveau des messages interceptés auparavant pour tromper le système.

3) On peut utiliser un nonce (numéro unique) ou un timestamp dans chaque message pour vérifier que les messages sont nouveaux et ne sont pas des copies renvoyées. Cela permet de bloquer les attaques par relecture.


# TTL 

1) Oui, la principale difference est l'ajout du TTL, les messages ont une durée de vie limitée et s'ils depassent cette limite, ils ne peuvent plus etre déchiffrés.

2) Le message sera rejeté car il sera considéré comme expiré. Le decalage du temps fait croire que le message a depassé sa durée de vie.

3) Oui ça aide à se proteger de l'attaque precedent. Les messages expirent rapidement, ce qui empeche un attaquant de reutiliser d'anciens messages interceptés. 

4) Cette methode peut rencontrer des problemes si les horloges des systemes ne sont pas synchronisés. De plus, si le TTL est trop long, cela laisse encore la possibilité d'une attaque 



# Regard Critique 

-La bibliotheque Fernet n'est pas conçue pour chiffrer des fichiers ou messages trop volumineux, ce qui peut poser probléme si on doit échanger de gros volumes de données. 

-Meme si la generation des IV avec os.urandom() est relativement securisée, un attaquant trés sophistiqué pourrait essayé de predire les IV sur un systeme mal securisé.

-Bien que les messages soient chiffrés, les noms des utilisateurs et l'historique d'envoi des messages reste visible. Un attaquant pourrait savoir qui communique avec qui meme sans connaitre le contenu des messages. On pourrait utiliser des protocoles qui permettent de chiffrer les metadonnées.

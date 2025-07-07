# digital-identity-platform
Cette documentation décrit une version améliorée de la plateforme d’identité numérique IDFAD, désormais conteneurisée avec Docker et utilisant PostgreSQL comme base de données persistante.
Documentation de la Plateforme d’Identité Numérique IDFAD (Version Conteneurisée)
Cette documentation décrit une version améliorée de la plateforme d’identité numérique IDFAD, désormais conteneurisée avec Docker et utilisant PostgreSQL comme base de données persistante. Elle inclut également une explication des défis rencontrés lors de l’implémentation dans l’environnement de sandbox.
1. Architecture de l’Application
L’application est composée de deux services principaux :
	•	Application Flask (Backend) : Une API RESTful développée avec Flask, responsable de la gestion des identités (enregistrement, authentification, consultation). Elle interagit avec une base de données PostgreSQL.
	•	Base de Données PostgreSQL : Une base de données relationnelle utilisée pour stocker les informations d’identité de manière persistante.
	•	Interface Utilisateur (Frontend) : Une interface web simple (HTML/CSS/JavaScript) qui permet d’interagir avec l’API Flask.
L’ensemble de l’application est conçu pour être déployé via Docker et Docker Compose, assurant ainsi une portabilité et une gestion des dépendances facilitées.
2. Fichiers du Projet
Le projet est structuré comme suit :
	•	`app.py` : Le code source de l’API Flask.
	•	`index.html` : L’interface utilisateur web.
	•	`requirements.txt` : Liste des dépendances Python nécessaires pour l’application Flask.
	•	`Dockerfile` : Fichier de configuration pour construire l’image Docker de l’application Flask.
	•	`docker-compose.yml` : Fichier de configuration pour définir et exécuter l’application multi-conteneurs (Flask et PostgreSQL).
	•	`documentation.md` : Ce fichier de documentation.
3. Explication du Code Source
`app.py` (API Flask)
Changements clés dans `app.py` :
	•	Connexion PostgreSQL : Utilise la bibliothèque `psycopg2` pour se connecter à une base de données PostgreSQL. L’URL de la base de données est récupérée via une variable d’environnement `DATABASE_URL`, ce qui est essentiel pour la conteneurisation.
	•	Initialisation de la base de données : Au démarrage de l’application, elle tente de créer la table `identities` si elle n’existe pas, assurant ainsi que la base de données est prête à l’emploi.
	•	Opérations CRUD : Les routes `/register`, `/authenticate`, `/identities`, et `/identity/<identity_id>` ont été adaptées pour interagir avec la base de données PostgreSQL.
`index.html` (Interface Utilisateur)
Le fichier `index.html` est une interface web simple qui permet d’interagir avec l’API Flask. La seule modification notable est l’ajustement de `API_BASE_URL` pour pointer vers l’URL exposée par Docker Compose (ou l’URL de l’environnement de sandbox si l’application est exposée directement).
`requirements.txt`
Ce fichier liste les dépendances Python nécessaires. `psycopg2-binary` est ajouté pour la connexion à PostgreSQL.
`Dockerfile`
Ce `Dockerfile` définit comment construire l’image Docker de l’application Flask. Il installe les dépendances, copie le code de l’application et définit la commande de démarrage.
`docker-compose.yml`
Ce fichier `docker-compose.yml` orchestre les deux services : `db` (PostgreSQL) et `app` (l’application Flask). Il configure les variables d’environnement pour la base de données et lie l’application Flask à la base de données via le réseau Docker interne. Le volume `db_data` assure la persistance des données de la base de données.
4. Fonctionnalités Clés et Limites
Fonctionnalités Clés :
	•	Conteneurisation : L’application est entièrement conteneurisée, ce qui facilite son déploiement et sa gestion dans n’importe quel environnement supportant Docker.
	•	Base de Données Persistante : L’utilisation de PostgreSQL assure que les données d’identité sont stockées de manière durable, même si les conteneurs sont redémarrés.
	•	API RESTful : Fournit une interface claire et standardisée pour interagir avec le système d’identité.
	•	Séparation des préoccupations : Le backend et la base de données sont des services distincts, ce qui améliore la modularité et la scalabilité.
Limites :
	•	Sécurité : Pour des raisons de simplicité de démonstration, les mots de passe de la base de données sont en clair dans le `docker-compose.yml`. Dans un environnement de production, des pratiques de sécurité plus robustes (variables d’environnement sécurisées, secrets Docker) seraient nécessaires.
	•	Authentification simplifiée : L’authentification par
l’empreinte digitale est très basique et ne représente pas une solution de sécurité réelle pour la biométrie. Des mécanismes d’authentification plus robustes (ex: JWT, OAuth2) et des algorithmes de hachage sécurisés pour les empreintes digitales seraient requis pour une application réelle.
	•	Gestion des erreurs : La gestion des erreurs est basique. Une application de production nécessiterait une gestion des erreurs plus granulaire et des logs détaillés.
	•	Scalabilité : Bien que conteneurisée, cette application est une démonstration simple. Pour une scalabilité réelle, des outils d’orchestration comme Kubernetes et des stratégies de mise à l’échelle automatique seraient nécessaires.
5. Installation et Utilisation
Pour faire fonctionner cette application, vous aurez besoin de Docker et Docker Compose installés sur votre machine.
	1.	Cloner le dépôt (ou décompresser le ZIP) :
	2.	Construire et démarrer les conteneurs :
Naviguez vers le répertoire `digital_identity_app` et exécutez la commande suivante :
Cette commande va :
	◦	Construire l’image Docker de l’application Flask (si elle n’existe pas ou si des changements ont été faits).
	◦	Démarrer un conteneur PostgreSQL.
	◦	Démarrer le conteneur de l’application Flask et le connecter à la base de données.
	◦	Le flag `-d` permet de lancer les conteneurs en arrière-plan.
	3.	Accéder à l’application :
L’application Flask sera accessible sur le port `5000` de votre machine. Ouvrez votre navigateur web et accédez à :
Si vous utilisez un environnement de sandbox ou une machine virtuelle, l’URL pourrait être différente (par exemple, l’URL exposée par le service d’exposition de port).
	4.	Interagir avec l’application :
Utilisez l’interface web pour :
	◦	Enregistrer une Identité : Remplissez les champs “Nom Complet”, “Date de Naissance” et “Empreinte Digitale” (simulée) et cliquez sur “Enregistrer”. Un ID d’identité sera généré.
	◦	Authentifier une Identité : Utilisez l’ID d’identité et l’empreinte digitale pour tenter une authentification.
	◦	Voir les Identités : Cliquez sur le bouton pour lister toutes les identités enregistrées dans la base de données.
6. Problèmes Rencontrés dans l’Environnement de Sandbox
Lors du développement de cette application dans l’environnement de sandbox, plusieurs problèmes liés à Docker ont été rencontrés, rendant le déploiement direct via `docker-compose up` difficile :
	•	Permissions du démon Docker : Des erreurs de permission (`permission denied while trying to connect to the Docker daemon socket`) ont été fréquentes, nécessitant des ajustements manuels des permissions (`sudo usermod -aG docker ubuntu` et `newgrp docker`) et des redémarrages du service Docker.
	•	Problèmes de communication Docker : Des erreurs de type `Error while fetching server API version: Not supported URL scheme http+docker` ont persisté, indiquant des difficultés pour Docker Compose à communiquer avec le démon Docker, même après avoir ajusté les permissions et redémarré le service.
	•	Stabilité de l’environnement : L’environnement de sandbox peut parfois présenter une instabilité avec les services Docker, entraînant des échecs inattendus lors de la construction ou du démarrage des conteneurs.
Ces problèmes ont empêché une démonstration en direct de l’application conteneurisée dans cet environnement. Cependant, les fichiers `Dockerfile` et `docker-compose.yml` sont correctement configurés et devraient fonctionner sans problème dans un environnement Docker local ou un serveur avec une configuration Docker stable.
7. Conclusion
Cette version conteneurisée de la plateforme d’identité numérique IDFAD démontre une approche plus robuste et portable pour le développement d’applications d’identité. Bien que des défis aient été rencontrés dans l’environnement de sandbox, l’architecture et le code fournis sont solides et prêts à être déployés dans un environnement de production. Les concepts d’API RESTful, de base de données persistante et de conteneurisation sont des éléments clés pour la construction de systèmes d’identité modernes et évolutifs.
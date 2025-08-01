#!/bin/bash

# Script de configuration de l'API pour le projet IDFAD
# Ce script guide l'utilisateur à travers la configuration de l'API MOSIP

echo "=== Script de configuration de l'API MOSIP pour le projet IDFAD ==="
echo "Ce script va vous guider à travers la configuration de l'API MOSIP."
echo ""

# Vérification des prérequis
echo "Vérification des prérequis..."
command -v git >/dev/null 2>&1 || { echo "Git est requis mais n'est pas installé. Veuillez l'installer."; exit 1; }
command -v java >/dev/null 2>&1 || { echo "Java est requis mais n'est pas installé. Veuillez installer Java 11 ou supérieur."; exit 1; }
command -v mvn >/dev/null 2>&1 || { echo "Maven est requis mais n'est pas installé. Veuillez l'installer."; exit 1; }

echo "Prérequis vérifiés avec succès."
echo ""

# Création du répertoire de travail
API_DIR="$HOME/mosip-api"
echo "Création du répertoire de travail pour l'API: $API_DIR"
mkdir -p "$API_DIR"
cd "$API_DIR"

# Clonage des dépôts API nécessaires
echo "Clonage des dépôts API MOSIP..."

# ID Repository API
echo "Clonage du dépôt ID Repository API..."
git clone https://github.com/mosip/id-repository.git
if [ $? -ne 0 ]; then
    echo "Erreur lors du clonage du dépôt ID Repository API."
    exit 1
fi

# Authentication API
echo "Clonage du dépôt Authentication API..."
git clone https://github.com/mosip/id-authentication.git
if [ $? -ne 0 ]; then
    echo "Erreur lors du clonage du dépôt Authentication API."
    exit 1
fi

# Commons API
echo "Clonage du dépôt Commons API..."
git clone https://github.com/mosip/commons.git
if [ $? -ne 0 ]; then
    echo "Erreur lors du clonage du dépôt Commons API."
    exit 1
fi

echo "Dépôts API MOSIP clonés avec succès."
echo ""

# Instructions pour la configuration de l'API
echo "=== Instructions pour la configuration de l'API ==="
echo "Pour configurer et déployer les API MOSIP, suivez ces étapes:"
echo "1. Configurez les propriétés d'application dans les fichiers de configuration"
echo "2. Compilez les projets avec Maven: mvn clean install"
echo "3. Déployez les services API sur votre serveur d'applications"
echo ""
echo "Note: Consultez la documentation spécifique à chaque module pour plus de détails."
echo ""

# Création d'un fichier de configuration personnalisé pour l'API
echo "Création d'un fichier de configuration personnalisé pour l'API IDFAD..."
mkdir -p "$API_DIR/config"

cat > "$API_DIR/config/application-idfad.properties" << 'EOLCONF'
# Configuration personnalisée pour le projet IDFAD

# Paramètres de base de données
mosip.kernel.database.hostname=localhost
mosip.kernel.database.port=5432
mosip.kernel.database.username=postgres
mosip.kernel.database.password=postgres

# Paramètres d'authentification
mosip.ida.auth.clientId=mosip-ida-client
mosip.ida.auth.secretKey=abc123
mosip.ida.auth.appId=IDA

# Paramètres biométriques
mosip.biometric.sdk.provider=mock
mosip.biometric.sdk.timeout=30

# Paramètres de localisation
mosip.supported.languages=fra,eng,ara
mosip.primary.language=fra

# Paramètres de notification
mosip.notification.email.from=no-reply@idfad.org
mosip.notification.sms.gateway=mock

# Paramètres de sécurité
mosip.kernel.crypto.asymmetric-algorithm-name=RSA/ECB/OAEPWITHSHA-256ANDMGF1PADDING
mosip.kernel.crypto.symmetric-algorithm-name=AES/GCM/PKCS5Padding
EOLCONF

echo "Fichier de configuration créé: $API_DIR/config/application-idfad.properties"
echo ""

# Création d'un script de démarrage rapide pour l'API
cat > "$API_DIR/start_api.sh" << 'EOLSTART'
#!/bin/bash

# Script de démarrage des API MOSIP pour le projet IDFAD

echo "Démarrage des API MOSIP pour le projet IDFAD..."

# Définition des variables d'environnement
export SPRING_PROFILES_ACTIVE=idfad
export SPRING_CONFIG_LOCATION=file:$HOME/mosip-api/config/

# Démarrage des services API (exemple)
echo "Démarrage du service ID Repository..."
cd $HOME/mosip-api/id-repository/id-repository-identity-service
java -jar target/id-repository-identity-service-*.jar &

echo "Démarrage du service Authentication..."
cd $HOME/mosip-api/id-authentication/authentication-service
java -jar target/authentication-service-*.jar &

echo "Les services API MOSIP sont en cours de démarrage."
echo "Consultez les logs pour plus de détails."
EOLSTART

chmod +x "$API_DIR/start_api.sh"
echo "Script de démarrage créé: $API_DIR/start_api.sh"
echo ""

echo "Configuration de l'API MOSIP pour le projet IDFAD terminée."
echo "Veuillez consulter la documentation officielle pour plus de détails: https://docs.mosip.io/platform/apis"

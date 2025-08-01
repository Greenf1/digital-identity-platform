#!/bin/bash

# Script d'installation de MOSIP pour le projet IDFAD
# Ce script guide l'utilisateur à travers les étapes d'installation de MOSIP

echo "=== Script d'installation de MOSIP pour le projet IDFAD ==="
echo "Ce script va vous guider à travers l'installation de MOSIP."
echo ""

# Vérification des prérequis
echo "Vérification des prérequis..."
command -v git >/dev/null 2>&1 || { echo "Git est requis mais n'est pas installé. Veuillez l'installer."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker est requis mais n'est pas installé. Veuillez l'installer."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose est requis mais n'est pas installé. Veuillez l'installer."; exit 1; }

echo "Prérequis vérifiés avec succès."
echo ""

# Création du répertoire de travail
WORK_DIR="$HOME/mosip-infra"
echo "Création du répertoire de travail: $WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Clonage du dépôt MOSIP
echo "Clonage du dépôt MOSIP..."
git clone https://github.com/mosip/mosip-infra.git .
if [ $? -ne 0 ]; then
    echo "Erreur lors du clonage du dépôt MOSIP."
    exit 1
fi

echo "Dépôt MOSIP cloné avec succès."
echo ""

# Navigation vers le répertoire de déploiement
echo "Navigation vers le répertoire de déploiement..."
cd deployment/sandbox-v2

# Vérification de l'existence du répertoire
if [ ! -d "$(pwd)" ]; then
    echo "Le répertoire de déploiement n'existe pas. La structure du dépôt a peut-être changé."
    exit 1
fi

echo "Vous êtes maintenant dans le répertoire de déploiement: $(pwd)"
echo ""

# Instructions pour le déploiement
echo "=== Instructions pour le déploiement ==="
echo "Pour déployer MOSIP, suivez ces étapes:"
echo "1. Configurez les variables d'environnement dans le fichier .env"
echo "2. Exécutez la commande: ./install.sh"
echo "3. Suivez les instructions à l'écran"
echo ""
echo "Note: Le déploiement peut prendre plusieurs heures selon votre connexion internet et les ressources de votre système."
echo ""

# Demande de confirmation pour continuer
read -p "Voulez-vous continuer avec l'installation? (o/n): " confirm
if [[ $confirm != [oO]* ]]; then
    echo "Installation annulée."
    exit 0
fi

echo "Lancement de l'installation..."
echo "Veuillez consulter la documentation officielle pour plus de détails: https://docs.mosip.io/"
echo ""

# Lancement de l'installation
./install.sh

echo "Script d'installation terminé."

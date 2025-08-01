# Guide d'Installation et de Déploiement - Plateforme IDFAD

**Développé par Greenfad**  
**Version**: 1.0.0  
**Date**: 17 juillet 2025  

## Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Prérequis Système](#prérequis-système)
3. [Installation Locale](#installation-locale)
4. [Configuration de Sécurité](#configuration-de-sécurité)
5. [Déploiement en Production](#déploiement-en-production)
6. [Maintenance et Monitoring](#maintenance-et-monitoring)
7. [Dépannage](#dépannage)
8. [Support Technique](#support-technique)

## Vue d'ensemble

La plateforme IDFAD (Identity Framework for African Development) est une solution complète d'identité numérique développée par Greenfad. Cette plateforme offre un système sécurisé et évolutif pour la gestion des identités nationales, conforme aux standards internationaux les plus stricts.

### Architecture de la Solution

La plateforme IDFAD est construite sur une architecture moderne composée de :

- **Backend API** : Développé en Python avec Flask, offrant des API REST sécurisées
- **Frontend Web** : Interface utilisateur moderne développée en React avec Tailwind CSS
- **Base de Données** : Système de stockage sécurisé avec chiffrement des données sensibles
- **Système de Sécurité** : Authentification multi-facteurs et audit complet

### Fonctionnalités Principales

- Enregistrement et gestion des identités citoyennes
- Support des données biométriques (empreintes, reconnaissance faciale, iris)
- Authentification multi-facteurs sécurisée
- Interface d'administration complète
- API REST pour l'intégration avec d'autres systèmes
- Conformité aux standards RGPD, ISO 27001 et NIST

## Prérequis Système

### Configuration Minimale

**Serveur de Développement :**
- CPU : 2 cœurs minimum, 4 cœurs recommandés
- RAM : 4 GB minimum, 8 GB recommandés
- Stockage : 20 GB d'espace libre minimum
- Système d'exploitation : Ubuntu 20.04+ ou CentOS 8+

**Serveur de Production :**
- CPU : 8 cœurs minimum, 16 cœurs recommandés
- RAM : 16 GB minimum, 32 GB recommandés
- Stockage : 100 GB SSD minimum avec sauvegarde
- Système d'exploitation : Ubuntu 22.04 LTS ou RHEL 9

### Logiciels Requis

**Environnement de Développement :**
- Python 3.11 ou supérieur
- Node.js 20.x ou supérieur
- npm ou pnpm (gestionnaire de paquets Node.js)
- Git 2.30 ou supérieur
- Navigateur web moderne (Chrome, Firefox, Safari)

**Base de Données :**
- SQLite (pour le développement)
- PostgreSQL 14+ (recommandé pour la production)
- Redis (pour la mise en cache et les sessions)

**Outils de Sécurité :**
- OpenSSL 3.0+ pour le chiffrement
- Certificats SSL/TLS valides pour la production
- Pare-feu configuré (UFW, iptables, ou équivalent)

## Installation Locale

### Étape 1 : Préparation de l'Environnement

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances système
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm git curl wget

# Installation de pnpm (gestionnaire de paquets Node.js)
npm install -g pnpm

# Vérification des versions
python3.11 --version
node --version
npm --version
git --version
```

### Étape 2 : Clonage du Projet

```bash
# Clonage du dépôt
git clone https://github.com/votre-organisation/digital-identity-platform.git
cd digital-identity-platform

# Vérification de la structure du projet
ls -la
```

### Étape 3 : Configuration du Backend

```bash
# Navigation vers le dossier backend
cd idfad-backend

# Création de l'environnement virtuel Python
python3.11 -m venv venv

# Activation de l'environnement virtuel
source venv/bin/activate

# Installation des dépendances Python
pip install -r requirements.txt

# Vérification de l'installation
pip list
```

### Étape 4 : Configuration de la Base de Données

```bash
# Création du dossier de base de données
mkdir -p src/database

# Initialisation de la base de données
python src/main.py &
sleep 5
pkill -f "python src/main.py"

# Vérification de la création de la base
ls -la src/database/
```

### Étape 5 : Configuration du Frontend

```bash
# Navigation vers le dossier frontend
cd ../idfad-frontend

# Installation des dépendances Node.js
pnpm install

# Vérification de l'installation
pnpm list
```

### Étape 6 : Démarrage des Services

**Terminal 1 - Backend :**
```bash
cd idfad-backend
source venv/bin/activate
python src/main.py
```

**Terminal 2 - Frontend :**
```bash
cd idfad-frontend
pnpm run dev --host
```

### Étape 7 : Vérification de l'Installation

1. **Test de l'API Backend :**
   - Ouvrir http://localhost:5000/api/health
   - Vérifier que le statut est "healthy"

2. **Test de l'Interface Frontend :**
   - Ouvrir http://localhost:5173
   - Vérifier que l'interface IDFAD se charge correctement

3. **Test de l'Intégration :**
   - Naviguer vers l'onglet "Enregistrement"
   - Tenter d'enregistrer un citoyen test
   - Vérifier que les données apparaissent dans le tableau de bord

## Configuration de Sécurité

### Chiffrement des Données

La plateforme IDFAD utilise plusieurs niveaux de chiffrement pour protéger les données sensibles :

**Chiffrement en Transit :**
- Tous les échanges utilisent HTTPS/TLS 1.3
- Certificats SSL/TLS avec validation étendue
- Perfect Forward Secrecy (PFS)

**Chiffrement au Repos :**
- Données biométriques chiffrées avec AES-256
- Hachage sécurisé des mots de passe avec bcrypt
- Clés de chiffrement stockées séparément

### Configuration des Certificats SSL

```bash
# Génération d'un certificat auto-signé pour le développement
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Pour la production, utiliser Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d votre-domaine.com
```

### Configuration du Pare-feu

```bash
# Configuration UFW pour Ubuntu
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5000/tcp  # Backend API (développement uniquement)
sudo ufw status
```

### Variables d'Environnement Sécurisées

Créer un fichier `.env` dans le dossier backend :

```bash
# Fichier .env pour la production
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
DATABASE_URL=postgresql://user:password@localhost:5432/idfad_prod
REDIS_URL=redis://localhost:6379/0
ENCRYPTION_KEY=clé-de-chiffrement-aes-256-bits
JWT_SECRET=secret-pour-les-tokens-jwt
ADMIN_EMAIL=admin@greenfad.com
SMTP_SERVER=smtp.greenfad.com
SMTP_PORT=587
SMTP_USERNAME=noreply@greenfad.com
SMTP_PASSWORD=mot-de-passe-smtp
```

## Déploiement en Production

### Option 1 : Déploiement avec Docker

**Dockerfile Backend :**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

**Dockerfile Frontend :**
```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY . .
RUN pnpm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
```

**Docker Compose :**
```yaml
version: '3.8'
services:
  backend:
    build: ./idfad-backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/idfad
    depends_on:
      - db
      - redis

  frontend:
    build: ./idfad-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: idfad
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Option 2 : Déploiement sur Serveur Dédié

**Configuration Nginx :**
```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name votre-domaine.com;

    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;

    # Configuration SSL sécurisée
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Frontend
    location / {
        root /var/www/idfad-frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API Backend
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Service Systemd pour le Backend :**
```ini
[Unit]
Description=IDFAD Backend API
After=network.target

[Service]
Type=simple
User=idfad
WorkingDirectory=/opt/idfad/backend
Environment=PATH=/opt/idfad/backend/venv/bin
ExecStart=/opt/idfad/backend/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Option 3 : Déploiement Cloud (AWS/Azure/GCP)

**Configuration Terraform pour AWS :**
```hcl
provider "aws" {
  region = "eu-west-1"
}

resource "aws_instance" "idfad_server" {
  ami           = "ami-0c94855ba95b798c7"  # Ubuntu 22.04 LTS
  instance_type = "t3.large"
  
  vpc_security_group_ids = [aws_security_group.idfad_sg.id]
  
  user_data = file("install_script.sh")
  
  tags = {
    Name = "IDFAD-Production-Server"
    Environment = "Production"
    Owner = "Greenfad"
  }
}

resource "aws_security_group" "idfad_sg" {
  name_prefix = "idfad-sg"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Maintenance et Monitoring

### Surveillance Système

**Monitoring avec Prometheus et Grafana :**
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

### Sauvegarde Automatisée

**Script de Sauvegarde :**
```bash
#!/bin/bash
# backup_idfad.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/idfad"
DB_NAME="idfad_prod"

# Création du dossier de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarde de la base de données
pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Sauvegarde des fichiers de configuration
tar -czf $BACKUP_DIR/config_backup_$DATE.tar.gz /opt/idfad/config/

# Sauvegarde des logs
tar -czf $BACKUP_DIR/logs_backup_$DATE.tar.gz /var/log/idfad/

# Nettoyage des anciennes sauvegardes (garde 30 jours)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Sauvegarde terminée : $DATE"
```

**Crontab pour automatisation :**
```bash
# Sauvegarde quotidienne à 2h du matin
0 2 * * * /opt/scripts/backup_idfad.sh >> /var/log/backup.log 2>&1

# Redémarrage hebdomadaire le dimanche à 3h
0 3 * * 0 systemctl restart idfad-backend
```

### Mise à Jour de Sécurité

**Script de Mise à Jour :**
```bash
#!/bin/bash
# update_idfad.sh

echo "Début de la mise à jour IDFAD..."

# Sauvegarde avant mise à jour
/opt/scripts/backup_idfad.sh

# Arrêt des services
systemctl stop idfad-backend
systemctl stop nginx

# Mise à jour du code
cd /opt/idfad
git pull origin main

# Mise à jour des dépendances backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Mise à jour des dépendances frontend
cd ../frontend
pnpm install
pnpm run build

# Migration de base de données si nécessaire
cd ../backend
python manage.py migrate

# Redémarrage des services
systemctl start idfad-backend
systemctl start nginx

# Vérification du statut
curl -f http://localhost:5000/api/health || echo "ERREUR: Backend non accessible"
curl -f http://localhost/api/health || echo "ERREUR: Frontend non accessible"

echo "Mise à jour terminée"
```

## Dépannage

### Problèmes Courants

**1. Erreur de Connexion à la Base de Données**
```bash
# Vérification du statut PostgreSQL
sudo systemctl status postgresql

# Vérification des logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Test de connexion
psql -h localhost -U postgres -d idfad_prod
```

**2. Erreur de Certificat SSL**
```bash
# Vérification du certificat
openssl x509 -in /etc/letsencrypt/live/votre-domaine.com/fullchain.pem -text -noout

# Renouvellement Let's Encrypt
sudo certbot renew --dry-run
```

**3. Problème de Performance**
```bash
# Monitoring des ressources
htop
iotop
netstat -tulpn

# Analyse des logs d'erreur
tail -f /var/log/idfad/error.log
tail -f /var/log/nginx/error.log
```

### Logs et Diagnostics

**Configuration des Logs :**
```python
# Configuration logging pour Flask
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('/var/log/idfad/app.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

**Analyse des Logs :**
```bash
# Recherche d'erreurs spécifiques
grep -i "error" /var/log/idfad/app.log | tail -20

# Analyse des tentatives d'authentification
grep "authentication" /var/log/idfad/app.log | grep "failure"

# Monitoring en temps réel
tail -f /var/log/idfad/app.log | grep -i "error\|warning"
```

## Support Technique

### Contact Greenfad

**Support Technique :**
- Email : support@greenfad.com
- Téléphone : +33 1 XX XX XX XX
- Site web : https://greenfad.com/support

**Support d'Urgence (24/7) :**
- Email : emergency@greenfad.com
- Téléphone : +33 6 XX XX XX XX

### Documentation Complémentaire

- **API Documentation** : https://docs.greenfad.com/idfad/api
- **Guide Administrateur** : https://docs.greenfad.com/idfad/admin
- **FAQ** : https://docs.greenfad.com/idfad/faq
- **Changelog** : https://docs.greenfad.com/idfad/changelog

### Formation et Certification

Greenfad propose des formations complètes pour l'administration et l'utilisation de la plateforme IDFAD :

- **Formation Administrateur** (3 jours)
- **Formation Développeur** (5 jours)
- **Certification IDFAD** (examen en ligne)

Pour plus d'informations : formation@greenfad.com

---

**© 2025 Greenfad. Tous droits réservés.**

*Ce document est confidentiel et propriétaire. Toute reproduction ou distribution non autorisée est strictement interdite.*


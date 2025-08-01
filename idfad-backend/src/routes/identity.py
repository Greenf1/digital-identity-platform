from flask import Blueprint, request, jsonify, current_app
from src.models.identity import db, CitizenIdentity, BiometricData, IdentityDocument, AuthenticationLog
from datetime import datetime, date
import uuid
import hashlib
import json
import base64
import os

identity_bp = Blueprint('identity', __name__)

@identity_bp.route('/health', methods=['GET'])
def health_check():
    """Point de contrôle de santé de l'API"""
    return jsonify({
        'status': 'healthy',
        'service': 'IDFAD Identity Service by Greenfad',
        'version': '1.0.0',
        'company': 'Greenfad',
        'timestamp': datetime.utcnow().isoformat()
    })

@identity_bp.route('/citizens', methods=['POST'])
def register_citizen():
    """Enregistrement d'un nouveau citoyen"""
    try:
        data = request.get_json()
        
        # Validation des données requises
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'place_of_birth', 'gender', 'address_line1', 'city', 'region']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        # Conversion de la date de naissance
        try:
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}), 400
        
        # Vérification de l'unicité (par nom, date de naissance et lieu)
        existing = CitizenIdentity.query.filter_by(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=dob,
            place_of_birth=data['place_of_birth']
        ).first()
        
        if existing:
            return jsonify({'error': 'Un citoyen avec ces informations existe déjà'}), 409
        
        # Création de la nouvelle identité
        citizen = CitizenIdentity(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            date_of_birth=dob,
            place_of_birth=data['place_of_birth'],
            gender=data['gender'],
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            address_line1=data['address_line1'],
            address_line2=data.get('address_line2'),
            city=data['city'],
            region=data['region'],
            postal_code=data.get('postal_code'),
            country=data.get('country', 'Cameroun'),
            father_name=data.get('father_name'),
            mother_name=data.get('mother_name'),
            marital_status=data.get('marital_status')
        )
        
        # Définition du PIN si fourni
        if 'pin' in data and data['pin']:
            citizen.set_pin(data['pin'])
        
        # Définition des questions de sécurité si fournies
        if 'security_questions' in data and data['security_questions']:
            citizen.set_security_questions(data['security_questions'])
        
        db.session.add(citizen)
        db.session.commit()
        
        return jsonify({
            'message': 'Citoyen enregistré avec succès',
            'citizen': citizen.to_dict(),
            'national_id': citizen.national_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur lors de l'enregistrement: {str(e)}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@identity_bp.route('/citizens/<citizen_id>', methods=['GET'])
def get_citizen(citizen_id):
    """Récupération des informations d'un citoyen"""
    try:
        citizen = CitizenIdentity.query.get(citizen_id)
        if not citizen:
            return jsonify({'error': 'Citoyen non trouvé'}), 404
        
        return jsonify({
            'citizen': citizen.to_dict(),
            'biometric_data': [bio.to_dict() for bio in citizen.biometric_data if bio.is_active],
            'documents': [doc.to_dict() for doc in citizen.documents]
        })
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération: {str(e)}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@identity_bp.route('/citizens/search', methods=['POST'])
def search_citizens():
    """Recherche de citoyens par critères"""
    try:
        data = request.get_json()
        query = CitizenIdentity.query
        
        # Filtres de recherche
        if 'national_id' in data and data['national_id']:
            query = query.filter(CitizenIdentity.national_id == data['national_id'])
        
        if 'first_name' in data and data['first_name']:
            query = query.filter(CitizenIdentity.first_name.ilike(f"%{data['first_name']}%"))
        
        if 'last_name' in data and data['last_name']:
            query = query.filter(CitizenIdentity.last_name.ilike(f"%{data['last_name']}%"))
        
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                query = query.filter(CitizenIdentity.date_of_birth == dob)
            except ValueError:
                return jsonify({'error': 'Format de date invalide'}), 400
        
        if 'phone_number' in data and data['phone_number']:
            query = query.filter(CitizenIdentity.phone_number == data['phone_number'])
        
        # Pagination
        page = data.get('page', 1)
        per_page = min(data.get('per_page', 10), 100)  # Limite à 100 résultats par page
        
        citizens = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'citizens': [citizen.to_dict() for citizen in citizens.items],
            'total': citizens.total,
            'pages': citizens.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la recherche: {str(e)}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@identity_bp.route('/citizens/<citizen_id>/biometric', methods=['POST'])
def add_biometric_data(citizen_id):
    """Ajout de données biométriques"""
    try:
        citizen = CitizenIdentity.query.get(citizen_id)
        if not citizen:
            return jsonify({'error': 'Citoyen non trouvé'}), 404
        
        data = request.get_json()
        
        # Validation des données requises
        required_fields = ['biometric_type', 'template_data', 'quality_score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        # Validation du type biométrique
        valid_types = ['fingerprint', 'face', 'iris']
        if data['biometric_type'] not in valid_types:
            return jsonify({'error': f'Type biométrique invalide. Types valides: {valid_types}'}), 400
        
        # Validation du score de qualité
        if not 0 <= data['quality_score'] <= 100:
            return jsonify({'error': 'Le score de qualité doit être entre 0 et 100'}), 400
        
        # Décodage des données biométriques (base64)
        try:
            template_binary = base64.b64decode(data['template_data'])
        except Exception:
            return jsonify({'error': 'Données biométriques invalides (base64 attendu)'}), 400
        
        # Désactivation des anciennes données du même type
        BiometricData.query.filter_by(
            citizen_id=citizen_id,
            biometric_type=data['biometric_type']
        ).update({'is_active': False})
        
        # Création de la nouvelle donnée biométrique
        biometric = BiometricData(
            citizen_id=citizen_id,
            biometric_type=data['biometric_type'],
            template_data=template_binary,
            quality_score=data['quality_score'],
            capture_device=data.get('capture_device')
        )
        
        db.session.add(biometric)
        db.session.commit()
        
        return jsonify({
            'message': 'Données biométriques ajoutées avec succès',
            'biometric': biometric.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur lors de l'ajout biométrique: {str(e)}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@identity_bp.route('/authenticate', methods=['POST'])
def authenticate():
    """Authentification d'un citoyen"""
    try:
        data = request.get_json()
        
        # Validation des données requises
        if 'national_id' not in data or 'auth_method' not in data:
            return jsonify({'error': 'national_id et auth_method sont requis'}), 400
        
        citizen = CitizenIdentity.query.filter_by(national_id=data['national_id']).first()
        if not citizen:
            return jsonify({'error': 'Citoyen non trouvé'}), 404
        
        if citizen.status != 'active':
            return jsonify({'error': 'Compte suspendu ou révoqué'}), 403
        
        auth_result = 'failure'
        auth_method = data['auth_method']
        
        # Authentification par PIN
        if auth_method == 'pin':
            if 'pin' not in data:
                return jsonify({'error': 'PIN requis pour cette méthode'}), 400
            
            if citizen.verify_pin(data['pin']):
                auth_result = 'success'
        
        # Authentification par question de sécurité
        elif auth_method == 'security_question':
            if 'question' not in data or 'answer' not in data:
                return jsonify({'error': 'Question et réponse requises'}), 400
            
            if citizen.verify_security_answer(data['question'], data['answer']):
                auth_result = 'success'
        
        # Authentification biométrique (simulation)
        elif auth_method == 'biometric':
            if 'biometric_type' not in data or 'template_data' not in data:
                return jsonify({'error': 'Type biométrique et données requises'}), 400
            
            # Ici, on simulerait la comparaison biométrique
            # Dans un vrai système, on comparerait avec les templates stockés
            biometric_data = citizen.biometric_data
            active_biometrics = [b for b in biometric_data if b.is_active and b.biometric_type == data['biometric_type']]
            
            if active_biometrics:
                # Simulation d'une correspondance réussie
                auth_result = 'success'
        
        else:
            return jsonify({'error': 'Méthode d\'authentification non supportée'}), 400
        
        # Calcul du score de risque (simulation)
        risk_score = calculate_risk_score(request, citizen, auth_method)
        
        # Enregistrement du log d'authentification
        auth_log = AuthenticationLog(
            citizen_id=citizen.id,
            auth_method=auth_method,
            auth_result=auth_result,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            service_requested=data.get('service_requested'),
            risk_score=risk_score
        )
        
        db.session.add(auth_log)
        db.session.commit()
        
        if auth_result == 'success':
            return jsonify({
                'message': 'Authentification réussie',
                'citizen_id': citizen.id,
                'national_id': citizen.national_id,
                'full_name': f"{citizen.first_name} {citizen.last_name}",
                'risk_score': risk_score,
                'session_token': generate_session_token(citizen.id)
            })
        else:
            return jsonify({'error': 'Authentification échouée'}), 401
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur lors de l'authentification: {str(e)}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@identity_bp.route('/citizens/<citizen_id>/status', methods=['PUT'])
def update_citizen_status(citizen_id):
    """Mise à jour du statut d'un citoyen"""
    try:
        citizen = CitizenIdentity.query.get(citizen_id)
        if not citizen:
            return jsonify({'error': 'Citoyen non trouvé'}), 404
        
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Le statut est requis'}), 400
        
        valid_statuses = ['active', 'suspended', 'revoked']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Statut invalide. Statuts valides: {valid_statuses}'}), 400
        
        citizen.status = data['status']
        citizen.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Statut mis à jour avec succès',
            'citizen': citizen.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur lors de la mise à jour du statut: {str(e)}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@identity_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Statistiques de la plateforme"""
    try:
        total_citizens = CitizenIdentity.query.count()
        active_citizens = CitizenIdentity.query.filter_by(status='active').count()
        suspended_citizens = CitizenIdentity.query.filter_by(status='suspended').count()
        revoked_citizens = CitizenIdentity.query.filter_by(status='revoked').count()
        
        # Statistiques biométriques
        total_biometric_records = BiometricData.query.filter_by(is_active=True).count()
        fingerprint_records = BiometricData.query.filter_by(biometric_type='fingerprint', is_active=True).count()
        face_records = BiometricData.query.filter_by(biometric_type='face', is_active=True).count()
        iris_records = BiometricData.query.filter_by(biometric_type='iris', is_active=True).count()
        
        # Statistiques d'authentification (dernières 24h)
        yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        recent_auths = AuthenticationLog.query.filter(AuthenticationLog.timestamp >= yesterday).count()
        successful_auths = AuthenticationLog.query.filter(
            AuthenticationLog.timestamp >= yesterday,
            AuthenticationLog.auth_result == 'success'
        ).count()
        
        return jsonify({
            'citizens': {
                'total': total_citizens,
                'active': active_citizens,
                'suspended': suspended_citizens,
                'revoked': revoked_citizens
            },
            'biometrics': {
                'total': total_biometric_records,
                'fingerprint': fingerprint_records,
                'face': face_records,
                'iris': iris_records
            },
            'authentication_24h': {
                'total_attempts': recent_auths,
                'successful': successful_auths,
                'success_rate': (successful_auths / recent_auths * 100) if recent_auths > 0 else 0
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des statistiques: {str(e)}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

def calculate_risk_score(request, citizen, auth_method):
    """Calcule un score de risque pour l'authentification"""
    risk_score = 0.0
    
    # Facteurs de risque basiques (simulation)
    # Dans un vrai système, cela serait beaucoup plus sophistiqué
    
    # Méthode d'authentification
    if auth_method == 'pin':
        risk_score += 30.0
    elif auth_method == 'security_question':
        risk_score += 40.0
    elif auth_method == 'biometric':
        risk_score += 10.0
    
    # Heure d'accès (plus de risque la nuit)
    current_hour = datetime.utcnow().hour
    if current_hour < 6 or current_hour > 22:
        risk_score += 20.0
    
    # Historique récent d'authentification
    recent_failures = AuthenticationLog.query.filter(
        AuthenticationLog.citizen_id == citizen.id,
        AuthenticationLog.auth_result == 'failure',
        AuthenticationLog.timestamp >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    
    risk_score += min(recent_failures * 15.0, 60.0)
    
    return min(risk_score, 100.0)

def generate_session_token(citizen_id):
    """Génère un token de session sécurisé"""
    # Dans un vrai système, on utiliserait JWT avec une clé secrète
    timestamp = str(int(datetime.utcnow().timestamp()))
    data = f"{citizen_id}:{timestamp}:{uuid.uuid4()}"
    return hashlib.sha256(data.encode()).hexdigest()[:32]


from src.models.user import db
from datetime import datetime
import uuid
import hashlib
import json

class CitizenIdentity(db.Model):
    """Modèle principal pour les identités citoyennes"""
    __tablename__ = 'citizen_identities'
    
    # Identifiant unique
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Numéro d'identité national unique
    national_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Informations démographiques de base
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    place_of_birth = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    
    # Informations de contact
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    
    # Adresse résidentielle
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=False, default='Cameroun')
    
    # Informations familiales
    father_name = db.Column(db.String(200), nullable=True)
    mother_name = db.Column(db.String(200), nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)
    
    # Statut et métadonnées
    status = db.Column(db.String(20), nullable=False, default='active')  # active, suspended, revoked
    enrollment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Informations de sécurité
    pin_hash = db.Column(db.String(255), nullable=True)  # Hash du PIN pour authentification
    security_questions = db.Column(db.Text, nullable=True)  # JSON des questions/réponses de sécurité
    
    # Relations
    biometric_data = db.relationship('BiometricData', backref='citizen', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('IdentityDocument', backref='citizen', lazy=True, cascade='all, delete-orphan')
    auth_logs = db.relationship('AuthenticationLog', backref='citizen', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(CitizenIdentity, self).__init__(**kwargs)
        if not self.national_id:
            self.national_id = self.generate_national_id()
    
    def generate_national_id(self):
        """Génère un numéro d'identité national unique"""
        # Format: YYYY-MM-DD-XXXX (date de naissance + 4 chiffres aléatoires)
        if self.date_of_birth:
            date_part = self.date_of_birth.strftime('%Y%m%d')
            random_part = str(uuid.uuid4().int)[:4]
            return f"{date_part}{random_part}"
        return str(uuid.uuid4().int)[:12]
    
    def set_pin(self, pin):
        """Définit le PIN de sécurité (hashé)"""
        self.pin_hash = hashlib.sha256(pin.encode()).hexdigest()
    
    def verify_pin(self, pin):
        """Vérifie le PIN de sécurité"""
        if not self.pin_hash:
            return False
        return self.pin_hash == hashlib.sha256(pin.encode()).hexdigest()
    
    def set_security_questions(self, questions_answers):
        """Définit les questions/réponses de sécurité"""
        # Hash des réponses pour la sécurité
        hashed_qa = {}
        for question, answer in questions_answers.items():
            hashed_qa[question] = hashlib.sha256(answer.lower().strip().encode()).hexdigest()
        self.security_questions = json.dumps(hashed_qa)
    
    def verify_security_answer(self, question, answer):
        """Vérifie une réponse à une question de sécurité"""
        if not self.security_questions:
            return False
        qa_dict = json.loads(self.security_questions)
        if question not in qa_dict:
            return False
        answer_hash = hashlib.sha256(answer.lower().strip().encode()).hexdigest()
        return qa_dict[question] == answer_hash
    
    def to_dict(self, include_sensitive=False):
        """Convertit l'objet en dictionnaire"""
        data = {
            'id': self.id,
            'national_id': self.national_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'place_of_birth': self.place_of_birth,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'email': self.email,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'region': self.region,
            'postal_code': self.postal_code,
            'country': self.country,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'marital_status': self.marital_status,
            'status': self.status,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
        
        if include_sensitive:
            data['has_pin'] = bool(self.pin_hash)
            data['has_security_questions'] = bool(self.security_questions)
        
        return data

class BiometricData(db.Model):
    """Modèle pour les données biométriques"""
    __tablename__ = 'biometric_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    citizen_id = db.Column(db.String(36), db.ForeignKey('citizen_identities.id'), nullable=False)
    
    # Type de biométrie
    biometric_type = db.Column(db.String(20), nullable=False)  # fingerprint, face, iris
    
    # Données biométriques (templates chiffrés)
    template_data = db.Column(db.LargeBinary, nullable=False)  # Template biométrique chiffré
    quality_score = db.Column(db.Float, nullable=False)  # Score de qualité (0-100)
    
    # Métadonnées
    capture_device = db.Column(db.String(100), nullable=True)
    capture_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'biometric_type': self.biometric_type,
            'quality_score': self.quality_score,
            'capture_device': self.capture_device,
            'capture_date': self.capture_date.isoformat() if self.capture_date else None,
            'is_active': self.is_active
        }

class IdentityDocument(db.Model):
    """Modèle pour les documents d'identité numérisés"""
    __tablename__ = 'identity_documents'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    citizen_id = db.Column(db.String(36), db.ForeignKey('citizen_identities.id'), nullable=False)
    
    # Type de document
    document_type = db.Column(db.String(50), nullable=False)  # birth_certificate, passport, etc.
    document_number = db.Column(db.String(100), nullable=True)
    
    # Données du document
    document_data = db.Column(db.LargeBinary, nullable=True)  # Document numérisé chiffré
    document_hash = db.Column(db.String(255), nullable=False)  # Hash pour vérification d'intégrité
    
    # Métadonnées
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_by = db.Column(db.String(100), nullable=True)
    verification_date = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'document_number': self.document_number,
            'document_hash': self.document_hash,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'verified': self.verified,
            'verified_by': self.verified_by,
            'verification_date': self.verification_date.isoformat() if self.verification_date else None
        }

class AuthenticationLog(db.Model):
    """Modèle pour les logs d'authentification"""
    __tablename__ = 'authentication_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    citizen_id = db.Column(db.String(36), db.ForeignKey('citizen_identities.id'), nullable=False)
    
    # Détails de l'authentification
    auth_method = db.Column(db.String(20), nullable=False)  # pin, biometric, otp
    auth_result = db.Column(db.String(20), nullable=False)  # success, failure, blocked
    
    # Contexte
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    service_requested = db.Column(db.String(100), nullable=True)
    
    # Métadonnées
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    risk_score = db.Column(db.Float, nullable=True)  # Score de risque calculé
    
    def to_dict(self):
        return {
            'id': self.id,
            'auth_method': self.auth_method,
            'auth_result': self.auth_result,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'service_requested': self.service_requested,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'risk_score': self.risk_score
        }


"""
API Flask pour Vacation Manager
Expose les endpoints REST pour le frontend
"""
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sys
import os
import json

# Ajouter le répertoire backend au chemin Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Models import User, Employee, VacationRequest, VacationStatus
from Database import DatabaseManager
from Services import AuthService, EmployeeService, VacationService

app = Flask(__name__)

# Activer CORS manuellement
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Initialiser les services
db = DatabaseManager("vacation_manager.db")
auth_service = AuthService(db)
employee_service = EmployeeService(db)
vacation_service = VacationService(db)


# ==================== AUTHENTIFICATION ====================

@app.route('/api/login', methods=['POST'])
def login():
    """Authentifier un utilisateur."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = auth_service.authenticate(email, password)
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Email ou mot de passe incorrect'
            }), 401

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Récupérer tous les utilisateurs."""
    try:
        users = db.get_all_users()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== EMPLOYÉS ====================

@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Récupérer tous les employés."""
    try:
        employees = db.get_all_employees()
        return jsonify({
            'success': True,
            'employees': [emp.to_dict() for emp in employees]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/employees/<int:user_id>', methods=['GET'])
def get_employee(user_id):
    """Récupérer un employé par user_id."""
    try:
        employee = employee_service.get_employee_by_user_id(user_id)
        if employee:
            return jsonify({
                'success': True,
                'employee': employee.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Employé non trouvé'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/employees', methods=['POST'])
def create_employee():
    """Créer un nouvel employé."""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        name = data.get('name')
        email = data.get('email')
        department = data.get('department', '')
        vacation_balance = int(data.get('vacation_balance', 20))
        
        employee = Employee(
            user_id=user_id,
            name=name,
            email=email,
            department=department,
            vacation_balance=vacation_balance
        )
        
        db.add_employee(employee)
        return jsonify({
            'success': True,
            'message': 'Employé créé avec succès',
            'employee': employee.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/employees/<int:user_id>', methods=['PUT'])
def update_employee(user_id):
    """Mettre à jour un employé."""
    try:
        data = request.get_json()
        employee = employee_service.get_employee_by_user_id(user_id)
        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'Employé non trouvé'
            }), 404
        
        # Mettre à jour les champs
        if 'name' in data:
            employee.name = data['name']
        if 'department' in data:
            employee.department = data['department']
        if 'vacation_balance' in data:
            employee.vacation_balance = int(data['vacation_balance'])
        
        db.update_employee(employee)
        return jsonify({
            'success': True,
            'message': 'Employé mise à jour',
            'employee': employee.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== DEMANDES DE CONGÉS ====================

@app.route('/api/vacation-requests', methods=['GET'])
def get_vacation_requests():
    """Récupérer tous les demandes de congés."""
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        
        requests_list = db.get_all_vacation_requests()
        
        # Filtrer par user_id si fourni
        if user_id:
            requests_list = [r for r in requests_list if r.employee_id == int(user_id)]
        
        # Filtrer par status si fourni
        if status:
            requests_list = [r for r in requests_list if r.status.value == status]
        
        return jsonify({
            'success': True,
            'vacation_requests': [req.to_dict() for req in requests_list]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/vacation-requests', methods=['POST'])
def create_vacation_request():
    """Créer une nouvelle demande de congés."""
    try:
        data = request.get_json()
        
        employee_id = int(data.get('employee_id'))
        start_date = datetime.fromisoformat(data.get('start_date')).date()
        end_date = datetime.fromisoformat(data.get('end_date')).date()
        reason = data.get('reason', '')
        
        # Valider les dates
        if not vacation_service.validate_dates(start_date, end_date):
            return jsonify({
                'success': False,
                'message': 'Dates invalides (début < fin, futur requis)'
            }), 400
        
        # Obtenir l'employé
        employee = db.get_employee_by_id(employee_id)
        if not employee:
            return jsonify({
                'success': False,
                'message': 'Employé non trouvé'
            }), 404
        
        # Calculer les jours
        days = vacation_service.calculate_days(start_date, end_date)
        
        # Créer la demande
        vacation_req = VacationRequest(
            id=None,
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            days_count=days,
            reason=reason
        )
        
        db.add_vacation_request(vacation_req)
        
        return jsonify({
            'success': True,
            'message': 'Demande de congés créée',
            'vacation_request': vacation_req.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/vacation-requests/<int:request_id>/approve', methods=['PUT'])
def approve_vacation_request(request_id):
    """Approuver une demande de congés."""
    try:
        data = request.get_json()
        approved_by = data.get('approved_by', 'admin')
        
        vacation_req = db.get_vacation_request_by_id(request_id)
        if not vacation_req:
            return jsonify({
                'success': False,
                'message': 'Demande non trouvée'
            }), 404
        
        # Valider le solde
        employee = db.get_employee_by_id(vacation_req.employee_id)
        if not vacation_service.has_enough_balance(employee, vacation_req.days_count):
            return jsonify({
                'success': False,
                'message': 'Solde insuffisant'
            }), 400
        
        # Approuver
        vacation_service.approve_request(request_id, approved_by)
        
        # Récupérer la demande mise à jour
        vacation_req = db.get_vacation_request_by_id(request_id)
        
        return jsonify({
            'success': True,
            'message': 'Demande approuvée',
            'vacation_request': vacation_req.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/vacation-requests/<int:request_id>/reject', methods=['PUT'])
def reject_vacation_request(request_id):
    """Rejeter une demande de congés."""
    try:
        data = request.get_json()
        reason = data.get('reason', '')
        
        vacation_req = db.get_vacation_request_by_id(request_id)
        if not vacation_req:
            return jsonify({
                'success': False,
                'message': 'Demande non trouvée'
            }), 404
        
        # Rejeter
        vacation_service.reject_request(request_id, reason)
        
        # Récupérer la demande mise à jour
        vacation_req = db.get_vacation_request_by_id(request_id)
        
        return jsonify({
            'success': True,
            'message': 'Demande rejetée',
            'vacation_request': vacation_req.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/vacation-requests/<int:request_id>/cancel', methods=['PUT'])
def cancel_vacation_request(request_id):
    """Annuler une demande de congés."""
    try:
        vacation_req = db.get_vacation_request_by_id(request_id)
        if not vacation_req:
            return jsonify({
                'success': False,
                'message': 'Demande non trouvée'
            }), 404
        
        # Annuler
        vacation_service.cancel_request(request_id)
        
        # Récupérer la demande mise à jour
        vacation_req = db.get_vacation_request_by_id(request_id)
        
        return jsonify({
            'success': True,
            'message': 'Demande annulée',
            'vacation_request': vacation_req.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== STATISTIQUES ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Récupérer les statistiques globales."""
    try:
        employees = db.get_all_employees()
        vacation_requests = db.get_all_vacation_requests()
        
        total_employees = len(employees)
        pending_requests = len([r for r in vacation_requests if r.status == VacationStatus.PENDING])
        approved_requests = len([r for r in vacation_requests if r.status == VacationStatus.APPROVED])
        rejected_requests = len([r for r in vacation_requests if r.status == VacationStatus.REJECTED])
        
        total_vacation_days = sum([emp.vacation_balance for emp in employees])
        total_used_days = sum([emp.vacation_used for emp in employees])
        
        return jsonify({
            'success': True,
            'stats': {
                'total_employees': total_employees,
                'pending_requests': pending_requests,
                'approved_requests': approved_requests,
                'rejected_requests': rejected_requests,
                'total_vacation_days': total_vacation_days,
                'total_used_days': total_used_days
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifier la santé de l'API."""
    return jsonify({
        'success': True,
        'message': 'API fonctionnelle',
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

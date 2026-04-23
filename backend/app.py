import os
import bcrypt
from pathlib import Path
from flask import Flask, request, jsonify, session, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_cors import CORS

from models import db, Department, User, Ticket, Comment, Attachment, TicketHistory
from auth import init_auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rzd-service-desk-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rzd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = str(Path(__file__).parent / 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

CORS(app, supports_credentials=True)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

db.init_app(app)
init_auth(app)

Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    login_val = data.get('login')
    password = data.get('password')

    user = User.query.filter_by(login=login_val).first()
    if not user:
        user = User.query.filter_by(email=login_val).first()

    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 401

    try:
        password_bytes = password.encode('utf-8')
        hash_bytes = user.password_hash.encode('utf-8')
        result = bcrypt.checkpw(password_bytes, hash_bytes)
        if result:
            login_user(user)
            return jsonify({'user': user.to_dict()})
        return jsonify({'error': 'Неверный пароль'}), 401
    except Exception as e:
        return jsonify({'error': f'Ошибка аутентификации: {str(e)}'}), 401


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})


@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    
    current_user.full_name = data.get('full_name', current_user.full_name)
    current_user.email = data.get('email', current_user.email)
    current_user.phone = data.get('phone', current_user.phone)
    current_user.department_id = data.get('department_id', current_user.department_id)
    
    if data.get('password'):
        new_password = data.get('password')
        password_bytes = new_password.encode('utf-8')
        salt_bytes = bcrypt.gensalt()
        current_user.password_hash = bcrypt.hashpw(password_bytes, salt_bytes).decode('utf-8')
    
    db.session.commit()
    return jsonify({'user': current_user.to_dict()})


@app.route('/api/test-auth', methods=['POST'])
def test_auth():
    data = request.get_json()
    login_val = data.get('login')
    password = data.get('password')
    
    user = User.query.filter_by(login=login_val).first()
    if not user:
        return jsonify({'error': 'User not found'}), 401
    
    return jsonify({
        'login': login_val,
        'password': password,
        'hash': user.password_hash,
        'hash_len': len(user.password_hash)
    })


@app.route('/api/me', methods=['GET'])
@login_required
def me():
    return jsonify({'user': current_user.to_dict()})


@app.route('/api/me/tickets', methods=['GET'])
@login_required
def my_tickets():
    tickets = Ticket.query.filter_by(created_by=current_user.id).order_by(Ticket.created_at.desc()).all()
    return jsonify({'tickets': [t.to_dict() for t in tickets]})


@app.route('/api/departments', methods=['GET'])
@login_required
def get_departments():
    departments = Department.query.all()
    return jsonify({'departments': [{'id': d.id, 'name': d.name, 'code': d.code} for d in departments]})


@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
    if current_user.role not in ['admin', 'specialist']:
        return jsonify({'error': 'Доступ запрещён'}), 403

    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]})


@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'user': user.to_dict()})


@app.route('/api/users', methods=['POST'])
@login_required
def create_user():
    if current_user.role != 'admin':
        return jsonify({'error': 'Доступ запрещён'}), 403

    data = request.get_json()
    required = ['login', 'password', 'role', 'full_name']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Отсутствует поле {field}'}), 400

    if User.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'Логин уже существует'}), 400

    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user = User(
        login=data['login'],
        email=data.get('email'),
        password_hash=password_hash,
        role=data['role'],
        full_name=data['full_name'],
        phone=data.get('phone'),
        department_id=data.get('department_id')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'user': user.to_dict()}), 201


@app.route('/api/tickets', methods=['GET'])
@login_required
def get_tickets():
    status = request.args.get('status')
    priority = request.args.get('priority')
    ticket_type = request.args.get('type')
    assigned_to_me = request.args.get('assigned_to_me')
    my_tickets = request.args.get('my_tickets')
    unassigned = request.args.get('unassigned')

    query = Ticket.query

    if assigned_to_me == 'true':
        query = query.filter(Ticket.assigned_to == current_user.id)

    if my_tickets == 'true':
        query = query.filter(Ticket.created_by == current_user.id)

    if unassigned == 'true':
        query = query.filter(Ticket.assigned_to == None)

    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if ticket_type:
        query = query.filter(Ticket.type == ticket_type)

    if current_user.role == 'employee':
        query = query.filter(Ticket.created_by == current_user.id)

    tickets = query.order_by(Ticket.created_at.desc()).all()
    return jsonify({'tickets': [t.to_dict() for t in tickets]})


@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
@login_required
def get_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return jsonify({'ticket': ticket.to_dict(include_relations=True)})


@app.route('/api/tickets', methods=['POST'])
@login_required
def create_ticket():
    data = request.get_json()

    required = ['title', 'type']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Отсутствует поле {field}'}), 400

    ticket = Ticket(
        title=data['title'],
        description=data.get('description'),
        type=data['type'],
        priority=data.get('priority', 'normal'),
        status='new',
        created_by=current_user.id,
        assigned_to=data.get('assigned_to')
    )
    db.session.add(ticket)
    db.session.flush()

    history = TicketHistory(
        ticket_id=ticket.id,
        field='status',
        old_value=None,
        new_value='new',
        changed_by=current_user.id
    )
    db.session.add(history)
    db.session.commit()

    return jsonify({'ticket': ticket.to_dict()}), 201


@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.get_json()

    if current_user.role == 'employee' and ticket.created_by != current_user.id:
        return jsonify({'error': 'Доступ запрещён'}), 403

    fields = ['title', 'description', 'type', 'priority', 'status', 'assigned_to']

    for field in fields:
        if field in data:
            old_value = getattr(ticket, field)
            new_value = data[field]

            if field == 'assigned_to' and new_value == '':
                new_value = None

            if old_value != new_value:
                if field in ['title', 'description']:
                    setattr(ticket, field, new_value)
                else:
                    history = TicketHistory(
                        ticket_id=ticket.id,
                        field=field,
                        old_value=str(old_value) if old_value else None,
                        new_value=str(new_value) if new_value else None,
                        changed_by=current_user.id
                    )
                    db.session.add(history)
                    setattr(ticket, field, new_value)

    ticket.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'ticket': ticket.to_dict(include_relations=True)})


@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_ticket(ticket_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Доступ запрещён'}), 403

    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/api/tickets/<int:ticket_id>/comments', methods=['GET'])
@login_required
def get_comments(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    comments = Comment.query.filter_by(ticket_id=ticket_id).order_by(Comment.created_at.asc()).all()
    return jsonify({'comments': [c.to_dict() for c in comments]})


@app.route('/api/tickets/<int:ticket_id>/comments', methods=['POST'])
@login_required
def create_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.get_json()

    if 'text' not in data:
        return jsonify({'error': 'Отсутствует текст комментария'}), 400

    comment = Comment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        text=data['text']
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({'comment': comment.to_dict()}), 201


@app.route('/api/tickets/<int:ticket_id>/attachments', methods=['POST'])
@login_required
def upload_attachment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if 'file' not in request.files:
        return jsonify({'error': 'Файл не загружен'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Недопустимый тип файла'}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f'{ticket_id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.{ext}'

    filepath = Path(app.config['UPLOAD_FOLDER']) / unique_name
    file.save(filepath)

    attachment = Attachment(
        ticket_id=ticket_id,
        filename=filename,
        filepath=unique_name
    )
    db.session.add(attachment)
    db.session.commit()

    return jsonify({'attachment': attachment.to_dict()}), 201


@app.route('/api/uploads/<path:filename>', methods=['GET'])
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_stats():
    tickets_query = Ticket.query

    if current_user.role == 'employee':
        tickets_query = tickets_query.filter(Ticket.created_by == current_user.id)
    elif current_user.role == 'specialist':
        tickets_query = tickets_query.filter(
            (Ticket.assigned_to == current_user.id) | (Ticket.created_by == current_user.id)
        )

    total = tickets_query.count()
    new_count = tickets_query.filter(Ticket.status == 'new').count()
    in_progress = tickets_query.filter(Ticket.status == 'in_progress').count()
    closed = tickets_query.filter(Ticket.status == 'closed').count()
    rejected = tickets_query.filter(Ticket.status == 'rejected').count()

    priority_stats = {}
    for priority in ['low', 'normal', 'high', 'critical']:
        priority_stats[priority] = tickets_query.filter(Ticket.priority == priority).count()

    type_stats = {}
    for ttype in ['equipment', 'software', 'access']:
        type_stats[ttype] = tickets_query.filter(Ticket.type == ttype).count()

    my_assigned = Ticket.query.filter(
        Ticket.assigned_to == current_user.id,
        Ticket.status.in_(['new', 'in_progress'])
    ).count()

    return jsonify({
        'total': total,
        'new': new_count,
        'in_progress': in_progress,
        'closed': closed,
        'rejected': rejected,
        'priority_stats': priority_stats,
        'type_stats': type_stats,
        'my_assigned': my_assigned
    })


@app.route('/api/admin/users', methods=['GET'])
@login_required
def admin_get_users():
    if current_user.role != 'admin':
        return jsonify({'error': 'Доступ запрещён'}), 403

    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]})


@app.route('/api/admin/departments', methods=['POST'])
@login_required
def admin_create_department():
    if current_user.role != 'admin':
        return jsonify({'error': 'Доступ запрещён'}), 403

    data = request.get_json()
    if 'name' not in data or 'code' not in data:
        return jsonify({'error': 'Отсутствует название или код'}), 400

    if Department.query.filter_by(code=data['code']).first():
        return jsonify({'error': 'Код подразделения уже существует'}), 400

    dept = Department(name=data['name'], code=data['code'])
    db.session.add(dept)
    db.session.commit()

    return jsonify({'department': {'id': dept.id, 'name': dept.name, 'code': dept.code}}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
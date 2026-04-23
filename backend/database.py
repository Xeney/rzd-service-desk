import os
import bcrypt
from models import db, Department, User, Ticket, Comment, Attachment, TicketHistory
from datetime import datetime, timedelta
import random


def init_db(app):
    with app.app_context():
        db.create_all()
        seed_departments()
        seed_users()
        seed_tickets()


def seed_departments():
    if Department.query.first():
        return

    departments_data = [
        ('Департамент информационных технологий', 'DIT'),
        ('Департамент кадров', 'DK'),
        ('Финансовый департамент', 'FIN'),
        ('Департамент логистики', 'DL'),
        ('Юридический департамент', 'UR'),
        ('Департамент маркетинга', 'DM'),
        ('Департамент продаж', 'DP'),
        ('Операционный департамент', 'OP'),
    ]

    for name, code in departments_data:
        dept = Department(name=name, code=code)
        db.session.add(dept)

    db.session.commit()


def seed_users():
    if User.query.first():
        return

    dit = Department.query.filter_by(code='DIT').first()
    dk = Department.query.filter_by(code='DK').first()
    fin = Department.query.filter_by(code='FIN').first()
    dl = Department.query.filter_by(code='DL').first()

    users_data = [
        ('admin', 'admin@tprzd.ru', 'admin', 'Иванов Иван Иванович', '+79001234567', dit.id),
        ('petrov', 'petrov@tprzd.ru', 'petrov', 'Петров Петр Петрович', '+79001234568', dit.id),
        ('smirnov', 'smirnov@tprzd.ru', 'smirnov', 'Смирнов Алексей Александрович', '+79001234569', dit.id),
        ('sidorov', 'sidorov@tprzd.ru', 'sidorov', 'Сидоров Алексей Алексеевич', '+79001234570', dk.id),
        ('kuznetsov', 'kuznetsov@tprzd.ru', 'kuznetsov', 'Кузнецов Дмитрий Сергеевич', '+79001234571', dk.id),
        ('volkov', 'volkov@tprzd.ru', 'volkov', 'Волков Максим Олегович', '+79001234572', fin.id),
        ('fedorov', 'fedorov@tprzd.ru', 'fedorov', 'Фёдоров Игорь Николаевич', '+79001234573', fin.id),
        ('mikhailov', 'mikhailov@tprzd.ru', 'mikhailov', 'Михайлов Сергей Петрович', '+79001234574', dl.id),
        ('romanov', 'romanov@tprzd.ru', 'romanov', 'Романов Антон Валерьевич', '+79001234575', dl.id),
    ]

    for login, email, password, full_name, phone, dept_id in users_data:
        if login == 'admin':
            role = 'admin'
        elif login in ['petrov', 'smirnov']:
            role = 'specialist'
        else:
            role = 'employee'

        password_bytes = password.encode('utf-8')
        salt_bytes = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt_bytes).decode('utf-8')

        user = User(
            login=login,
            email=email,
            password_hash=password_hash,
            role=role,
            full_name=full_name,
            phone=phone,
            department_id=dept_id
        )
        db.session.add(user)

    db.session.commit()


def seed_tickets():
    if Ticket.query.first():
        return

    employees = User.query.filter_by(role='employee').all()
    specialists = User.query.filter_by(role='specialist').all()
    admin = User.query.filter_by(role='admin').first()

    ticket_templates = [
        {'title': 'Не работает принтер в кабинете 305', 'description': 'Принтер HP LaserJet не включается, индикаторы не горят. Требуется ремонт или замена.', 'type': 'equipment', 'priority': 'normal'},
        {'title': 'Требуется доступ к CRM системе', 'description': 'Нужны права менеджера для работы с клиентской базой данных.', 'type': 'access', 'priority': 'high'},
        {'title': 'Установка Windows 11 на рабочий ПК', 'description': 'Компьютер Dell OptiPlex 7090, требуется обновление ОС до Windows 11 Pro.', 'type': 'software', 'priority': 'low'},
        {'title': 'Замена клавиатуры', 'description': 'Клавиша Enter не работает, клавиатура старая. Прошу заменить на новую.', 'type': 'equipment', 'priority': 'low'},
        {'title': 'Настройка почтового клиента', 'description': 'Не приходят письма на Outlook, исходящие работают. Ошибок не показывает.', 'type': 'software', 'priority': 'high'},
        {'title': 'Доступ к файловому серверу', 'description': 'Нужен доступ к папке /shared/docs для отдела кадров.', 'type': 'access', 'priority': 'normal'},
        {'title': 'Монитор показывает полосы', 'description': 'На мониторе LG 27UK850 появились горизонтальные полосы. Возможно, кабель.', 'type': 'equipment', 'priority': 'critical'},
        {'title': 'Установка 1С:ЗУП', 'description': 'Требуется установить 1С:Зарплата и управление кадрами версия 3.1.', 'type': 'software', 'priority': 'high'},
        {'title': 'Создание почтового ящика', 'description': 'Новому сотруднику нужен корпоративный email: ivanova@rzd.ru', 'type': 'access', 'priority': 'normal'},
        {'title': 'Ремонт ноутбука', 'description': 'Ноутбук Lenovo ThinkPad не загружается, черный экран после BIOS.', 'type': 'equipment', 'priority': 'high'},
    ]

    statuses = ['new', 'in_progress', 'closed', 'rejected']
    priorities = ['low', 'normal', 'high', 'critical']
    ticket_types = ['equipment', 'software', 'access']

    for i, template in enumerate(ticket_templates):
        creator = random.choice(employees)
        assigned = random.choice(specialists) if random.random() > 0.3 else None
        status = random.choice(statuses) if i > 2 else 'new'

        ticket = Ticket(
            title=template['title'],
            description=template['description'],
            type=template['type'],
            priority=template['priority'],
            status=status,
            created_by=creator.id,
            assigned_to=assigned.id if assigned else None,
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        )
        db.session.add(ticket)
        db.session.flush()

        if assigned and status != 'new':
            history = TicketHistory(
                ticket_id=ticket.id,
                field='status',
                old_value='new',
                new_value=status,
                changed_by=assigned.id
            )
            db.session.add(history)

        if i < 3 and specialists:
            for j in range(random.randint(1, 3)):
                comment_user = assigned if assigned else specialists[0]
                comment = Comment(
                    ticket_id=ticket.id,
                    user_id=comment_user.id,
                    text=f'Комментарий #{j+1} по заявке: рассматриваем вопрос.',
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 5))
                )
                db.session.add(comment)

    db.session.commit()


if __name__ == '__main__':
    from app import app
    init_db(app)
    print('Database initialized successfully!')
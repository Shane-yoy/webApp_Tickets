from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import User, Enterprise
from werkzeug.security import generate_password_hash
from app.decorators import role_required

admin_users_bp = Blueprint('admin_users', __name__)

# Affichage + ajout + édition + suppression dans une seule vue
@admin_users_bp.route('/admin/users', methods=['GET', 'POST'])
@role_required('admin')
def list_users():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            name = request.form['name']
            email = request.form['email']
            role = request.form['role']
            enterprise_id = request.form['enterprise_id']
            password = request.form['password']
            hashed_pw = generate_password_hash(password)

            new_user = User(name=name, email=email, role=role, enterprise_id=enterprise_id, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('admin_users.list_users'))

    users = User.query.all()
    enterprises = Enterprise.query.all()
    return render_template('admin_users.html', users=users, enterprises=enterprises)

# Update (là pour exemple mais mieux en page dédiée si beaucoup de champs)
@admin_users_bp.route('/admin/users/update/<int:user_id>', methods=['POST'])
@role_required('admin')
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.name = request.form.get('name', user.name)
    user.email = request.form.get('email', user.email)
    user.role = request.form.get('role', user.role)
    user.enterprise_id = request.form.get('enterprise_id', user.enterprise_id)
    db.session.commit()
    return redirect(url_for('admin_users.list_users'))

# Suppression
@admin_users_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_users.list_users'))

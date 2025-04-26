from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Enterprise
from app.decorators import role_required

admin_enterprises_bp = Blueprint('admin_enterprises', __name__)

@admin_enterprises_bp.route('/admin/enterprises', methods=['GET', 'POST'])
@role_required('admin') 
def list_enterprises():
    if request.method == 'POST':
          name = request.form['name']
          if name:
              new_enterprise = Enterprise(name=name)
              db.session.add(new_enterprise)
              db.session.commit()
              return redirect(url_for('admin_enterprises.list_enterprises'))

    enterprises = Enterprise.query.all()
    return render_template('admin_enterprises.html', enterprises=enterprises)

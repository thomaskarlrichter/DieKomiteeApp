import os
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from models import db, User, Wortmeldung, Rueckmeldung


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-secret-key-bitte-aendern-in-produktion'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///wortmeldung.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True

    db.init_app(app)
    CSRFProtect(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Bitte melde dich an, um diese Seite zu sehen.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    # ------------------------------------------------------------------
    # Auth Routes
    # ------------------------------------------------------------------

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            password2 = request.form.get('password2', '')

            error = None
            if not username or len(username) < 3:
                error = 'Benutzername muss mindestens 3 Zeichen lang sein.'
            elif not email or '@' not in email:
                error = 'Bitte gib eine gültige E-Mail-Adresse ein.'
            elif len(password) < 6:
                error = 'Das Passwort muss mindestens 6 Zeichen lang sein.'
            elif password != password2:
                error = 'Die Passwörter stimmen nicht überein.'
            elif User.query.filter_by(username=username).first():
                error = 'Dieser Benutzername ist bereits vergeben.'
            elif User.query.filter_by(email=email).first():
                error = 'Diese E-Mail-Adresse ist bereits registriert.'

            if error:
                flash(error, 'danger')
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Registrierung erfolgreich! Bitte melde dich jetzt an.', 'success')
                return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            remember = request.form.get('remember') == 'on'

            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                flash('Ungültiger Benutzername oder Passwort.', 'danger')
            else:
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                flash(f'Willkommen zurück, {user.username}!', 'success')
                return redirect(next_page or url_for('index'))

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Du wurdest erfolgreich abgemeldet.', 'info')
        return redirect(url_for('index'))

    # ------------------------------------------------------------------
    # Feed
    # ------------------------------------------------------------------

    @app.route('/')
    def index():
        page = request.args.get('page', 1, type=int)
        wortmeldungen = Wortmeldung.query.order_by(
            Wortmeldung.datum_uhrzeit.desc()
        ).paginate(page=page, per_page=10)
        return render_template('index.html', wortmeldungen=wortmeldungen)

    # ------------------------------------------------------------------
    # Profil
    # ------------------------------------------------------------------

    @app.route('/user/<username>')
    def profil(username):
        user = User.query.filter_by(username=username).first_or_404()
        page = request.args.get('page', 1, type=int)
        wortmeldungen = Wortmeldung.query.filter_by(user_id=user.id).order_by(
            Wortmeldung.datum_uhrzeit.desc()
        ).paginate(page=page, per_page=10)
        return render_template('profile.html', profil_user=user, wortmeldungen=wortmeldungen)

    # ------------------------------------------------------------------
    # Wortmeldungen
    # ------------------------------------------------------------------

    @app.route('/wortmeldung/neu', methods=['GET', 'POST'])
    @login_required
    def wortmeldung_neu():
        if request.method == 'POST':
            text = request.form.get('text', '').strip()
            if not text:
                flash('Die Wortmeldung darf nicht leer sein.', 'danger')
            elif len(text) > 2000:
                flash('Die Wortmeldung darf maximal 2000 Zeichen lang sein.', 'danger')
            else:
                wm = Wortmeldung(text=text, user_id=current_user.id)
                db.session.add(wm)
                db.session.commit()
                flash('Wortmeldung erfolgreich erstellt.', 'success')
                return redirect(url_for('wortmeldung_detail', wm_id=wm.id))
        return render_template('wortmeldung_neu.html')

    @app.route('/wortmeldung/<int:wm_id>')
    def wortmeldung_detail(wm_id):
        wm = Wortmeldung.query.get_or_404(wm_id)
        rueckmeldungen = Rueckmeldung.query.filter_by(
            wortmeldung_id=wm_id
        ).order_by(Rueckmeldung.datum_uhrzeit.asc()).all()
        return render_template('wortmeldung.html', wm=wm, rueckmeldungen=rueckmeldungen)

    @app.route('/wortmeldung/<int:wm_id>/loeschen', methods=['POST'])
    @login_required
    def wortmeldung_loeschen(wm_id):
        wm = Wortmeldung.query.get_or_404(wm_id)
        if wm.user_id != current_user.id:
            abort(403)
        db.session.delete(wm)
        db.session.commit()
        flash('Wortmeldung wurde gelöscht.', 'info')
        return redirect(url_for('profil', username=current_user.username))

    # ------------------------------------------------------------------
    # Rueckmeldungen
    # ------------------------------------------------------------------

    @app.route('/wortmeldung/<int:wm_id>/rueckmeldung', methods=['POST'])
    @login_required
    def rueckmeldung_erstellen(wm_id):
        Wortmeldung.query.get_or_404(wm_id)
        text = request.form.get('text', '').strip()
        if not text:
            flash('Die Rückmeldung darf nicht leer sein.', 'danger')
        elif len(text) > 1000:
            flash('Die Rückmeldung darf maximal 1000 Zeichen lang sein.', 'danger')
        else:
            rb = Rueckmeldung(text=text, user_id=current_user.id, wortmeldung_id=wm_id)
            db.session.add(rb)
            db.session.commit()
            flash('Rückmeldung erfolgreich gespeichert.', 'success')
        return redirect(url_for('wortmeldung_detail', wm_id=wm_id))

    @app.route('/rueckmeldung/<int:rb_id>/loeschen', methods=['POST'])
    @login_required
    def rueckmeldung_loeschen(rb_id):
        rb = Rueckmeldung.query.get_or_404(rb_id)
        wm_id = rb.wortmeldung_id
        if rb.user_id != current_user.id:
            abort(403)
        db.session.delete(rb)
        db.session.commit()
        flash('Rückmeldung wurde gelöscht.', 'info')
        return redirect(url_for('wortmeldung_detail', wm_id=wm_id))

    # ------------------------------------------------------------------
    # Error handlers
    # ------------------------------------------------------------------

    @app.errorhandler(403)
    def forbidden(e):
        return render_template(
            'error.html', code=403,
            message='Zugriff verweigert. Du hast keine Berechtigung für diese Aktion.'
        ), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template(
            'error.html', code=404,
            message='Seite nicht gefunden.'
        ), 404

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

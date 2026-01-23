# run the app
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///issues.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, faculty, admin
    issues = db.relationship('Issue', backref='author', lazy=True)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # technical, academic, facility
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, resolved
    faculty_response = db.Column(db.Text)
    resolution_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback = db.relationship('Feedback', backref='issue', lazy=True, uselist=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 rating
    comment = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False, unique=True)

def create_default_users():
    # Check if users already exist
    if User.query.first() is None:
        # Create default users for each role
        default_users = [
            {'username': 'student1', 'password': 'student123', 'role': 'student'},
            {'username': 'faculty1', 'password': 'faculty123', 'role': 'faculty'},
            {'username': 'admin1', 'password': 'admin123', 'role': 'admin'}
        ]
        
        for user_data in default_users:
            user = User(
                username=user_data['username'],
                password=generate_password_hash(user_data['password'], method='scrypt'),
                role=user_data['role']
            )
            db.session.add(user)
        
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        issues = Issue.query.filter_by(user_id=current_user.id).all()
        return render_template('student_dashboard.html', issues=issues)
    elif current_user.role == 'faculty':
        issues = Issue.query.filter(Issue.status.in_(['pending', 'in_progress'])).all()
        return render_template('faculty_dashboard.html', issues=issues)
    else:  # admin
        issues = Issue.query.all()
        return render_template('admin_dashboard.html', issues=issues)

@app.route('/report-issue', methods=['GET', 'POST'])
@login_required
def report_issue():
    if current_user.role != 'student':
        flash('Only students can report issues')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        issue = Issue(
            title=request.form['title'],
            description=request.form['description'],
            type=request.form['type'],
            user_id=current_user.id
        )
        db.session.add(issue)
        db.session.commit()
        flash('Issue reported successfully')
        return redirect(url_for('dashboard'))
    return render_template('report_issue.html')

@app.route('/update-issue/<int:issue_id>', methods=['POST'])
@login_required
def update_issue(issue_id):
    if current_user.role != 'faculty':
        flash('Only faculty can update issues')
        return redirect(url_for('dashboard'))
    
    issue = Issue.query.get_or_404(issue_id)
    issue.status = request.form['status']
    issue.faculty_response = request.form['faculty_response']
    
    if request.form['status'] == 'resolved':
        issue.resolution_date = datetime.utcnow()
    
    db.session.commit()
    flash('Issue updated successfully')
    return redirect(url_for('dashboard'))

@app.route('/submit-feedback/<int:issue_id>', methods=['POST'])
@login_required
def submit_feedback(issue_id):
    if current_user.role != 'student':
        flash('Only students can submit feedback')
        return redirect(url_for('dashboard'))
    
    issue = Issue.query.get_or_404(issue_id)
    if issue.user_id != current_user.id:
        flash('You can only provide feedback for your own issues')
        return redirect(url_for('dashboard'))
    
    if issue.status != 'resolved':
        flash('You can only provide feedback for resolved issues')
        return redirect(url_for('dashboard'))
    
    if issue.feedback:
        flash('Feedback has already been submitted for this issue')
        return redirect(url_for('dashboard'))
    
    feedback = Feedback(
        rating=int(request.form['rating']),
        comment=request.form['comment'],
        issue_id=issue_id
    )
    db.session.add(feedback)
    db.session.commit()
    flash('Thank you for your feedback')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_users()
    app.run(debug=True)
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask import abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.utils import secure_filename

# ── Initialize ──
app = Flask(__name__)
CORS(app)

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASEDIR, 'characters.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

ALLOWED_EXTS = {'png','jpg','jpeg','gif'}

db = SQLAlchemy(app)

# ── Model ──
class Character(db.Model):
    __tablename__  = 'characters'
    # id             = db.Column(db.Integer, primary_key=True)
    # name           = db.Column(db.String(100), nullable=False)
    # class_name     = db.Column(db.String(50),  nullable=False)
    # level          = db.Column(db.Integer,      nullable=False)
    # professions    = db.Column(db.String(200))            # comma‑sep
    # photo_filename = db.Column(db.String(200))            # stored filename

    id:                 Mapped[int]     = mapped_column(Integer, primary_key=True)
    name:               Mapped[str]     = mapped_column(String(100), nullable=False)
    class_name:         Mapped[str]     = mapped_column("class_name", String(50), nullable=False)
    spec_name:          Mapped[str]     = mapped_column("spec_name", String(50), nullable=False)
    level:              Mapped[int]     = mapped_column(Integer, nullable=False)
    professions:        Mapped[str]     = mapped_column(String(200))    # comma-sep list
    photo_filename:     Mapped[str]     = mapped_column(String(200), nullable=True)    # stored filename

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'class':       self.class_name,
            'spec':        self.spec_name,
            'level':       self.level,
            'professions': (self.professions or '').split(','),
            'photo_url':   url_for('uploaded_file',
                                   filename=self.photo_filename,
                                   _external=True)
                         if self.photo_filename else None
        }

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.',1)[1].lower() in ALLOWED_EXTS

# ── Routes ──
@app.route('/api/characters', methods=['GET'])
def list_characters():
    return jsonify([c.to_dict() for c in Character.query.all()])

@app.route('/api/characters', methods=['POST'])
def add_character():
    # Expect multipart/form-data
    name        = request.form.get('name')
    class_name  = request.form.get('class')
    spec_name   = request.form.get('spec')
    level       = request.form.get('level')
    profs       = request.form.get('professions','')

    if not (name and class_name and level):
        return jsonify({'error':'Missing fields'}), 400

    char = Character(
        name        = name,
        class_name  = class_name,
        spec_name   = spec_name,
        level       = int(level),
        professions = profs
    )

    # Handle uploaded photo
    file = request.files.get('photo')
    if file and allowed_file(file.filename):
        secure = secure_filename(file.filename)
        path   = os.path.join(app.config['UPLOAD_FOLDER'], secure)
        file.save(path)
        char.photo_filename = secure

    db.session.add(char)
    db.session.commit()
    return jsonify(char.to_dict()), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# … after your existing routes …

# 1.a GET a single character
@app.route('/api/characters/<int:char_id>', methods=['GET'])
def get_character(char_id):
    char = Character.query.get_or_404(char_id)
    return jsonify(char.to_dict())

# 1.b PATCH to update one or more fields
@app.route('/api/characters/<int:char_id>', methods=['PATCH'])
def update_character(char_id):
    char = Character.query.get_or_404(char_id)

    # expect JSON body
    data = request.get_json() or {}

    # only allow these fields
    if 'level' in data:
        try:
            char.level = int(data['level'])
        except ValueError:
            return jsonify({'error':'Level must be an integer'}), 400

    if 'professions' in data:
        # accept either list or comma‑sep string
        profs = data['professions']
        if isinstance(profs, list):
            profs = ','.join(p.strip() for p in profs if p.strip())
        char.professions = profs

    db.session.commit()
    return jsonify(char.to_dict())

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

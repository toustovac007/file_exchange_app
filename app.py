from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# ====== KONFIGURACE ======
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "/uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["APPLICATION_ROOT"] = "/file_exchange"


app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
ALLOWED_MIME_TYPES = {
    'text/plain',
    'application/pdf',
    'image/png',
    'image/jpeg'
}




class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<UploadedFile {self.filename}>"




# ====== VALIDACE ======
def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# ====== ROUTY ======
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/files')
def files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files.html', files=files)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')

        # 1️ kontrola, zda byl vybrán soubor
        if not file or file.filename == "":
            return "Nebyl vybrán žádný soubor", 400

        # 2️ kontrola přípony souboru
        if not allowed_file(file.filename):
            return "Nepovolená přípona souboru", 400

        # 3️ kontrola MIME typu
        if file.mimetype not in ALLOWED_MIME_TYPES:
            return "Nepovolený MIME typ souboru", 400

        # 4️ bezpečný název souboru
        filename = secure_filename(file.filename)

        # 5️ uložení souboru
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))



        new_file = UploadedFile(filename=filename)
        db.session.add(new_file)
        db.session.commit()

        return redirect(url_for('files'))

    return render_template('upload.html')



@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# ====== CHYBA – PŘÍLIŠ VELKÝ SOUBOR ======
@app.errorhandler(413)
def too_large(e):
    return "Soubor je příliš velký (max 5 MB)", 413

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', debug=True)
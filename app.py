import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from ldap3 import Server, Connection, LDAPBindError, LDAPSocketOpenError
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Détecter si l'application est exécutée depuis un exécutable PyInstaller
if getattr(sys, 'frozen', False):
    # Si l'application est en mode exécutable
    base_path = sys._MEIPASS
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # Si l'application est en mode développement
    app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limiter la taille des fichiers à 16 Mo

# Créer le dossier de téléchargement s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_excel(file):
    """Valide le fichier Excel téléchargé."""
    if not allowed_file(file.filename):
        return "Format du fichier non autorisé"
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        df = pd.read_excel(file_path)
        if 'Nom Complet' not in df.columns:
            return "La colonne 'Nom Complet' est manquante dans le fichier"
    except Exception as e:
        return f"Erreur lors de la lecture du fichier Excel : {str(e)}"
    
    return None

def compare_excel_to_ad(excel_file):
    """Compare les noms du fichier Excel avec l'Active Directory."""
    try:
        df = pd.read_excel(excel_file)
        if 'Nom Complet' not in df.columns:
            return "Erreur : La colonne 'Nom Complet' n'a pas été trouvée dans le fichier Excel.", []

        names_to_check = df['Nom Complet'].tolist()
        results = []
        ldap_error = None

        try:
            server = Server(app.config['LDAP_HOST'], port=app.config['LDAP_PORT'], use_ssl=app.config['LDAP_USE_SSL'])
            conn = Connection(server, user=app.config['LDAP_BIND_USER_DN'], password=app.config['LDAP_BIND_USER_PASSWORD'], auto_bind=True)

            if not conn.bind():
                ldap_error = f"Erreur d'authentification LDAP : {conn.last_error}"
            else:
                for name in names_to_check:
                    search_filter = f'(&(objectClass=person)(cn={name}))'
                    try:
                        conn.search(
                            search_base=app.config['LDAP_BASE_DN'],
                            search_filter=search_filter,
                            search_scope=app.config['LDAP_SEARCH_SCOPE'],
                            attributes=['cn']
                        )
                        if conn.entries:
                            results.append({'name_excel': name, 'found_in_ad': True, 'ad_info': conn.entries[0].entry_attributes_as_dict})
                        else:
                            results.append({'name_excel': name, 'found_in_ad': False, 'ad_info': None})
                    except Exception as e:
                        results.append({'name_excel': name, 'found_in_ad': 'Erreur lors de la recherche', 'ad_info': str(e)})
                conn.unbind()

        except LDAPBindError as e:
            ldap_error = f"Erreur de liaison LDAP : {e}"
        except LDAPSocketOpenError as e:
            ldap_error = f"Erreur de connexion au serveur LDAP : {e}"
        except Exception as e:
            ldap_error = f"Une erreur LDAP inattendue s'est produite : {e}"

        return ldap_error, results

    except FileNotFoundError:
        return "Erreur : Le fichier Excel n'a pas été trouvé.", []
    except pd.errors.EmptyDataError:
        return "Erreur : Le fichier Excel est vide.", []
    except KeyError as e:
        return f"Erreur : La colonne '{e}' n'a pas été trouvée dans le fichier Excel.", []
    except Exception as e:
        return f"Une erreur inattendue s'est produite lors du traitement du fichier : {e}", []

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Route pour télécharger et traiter le fichier Excel."""
    error = None
    results = []
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'Aucun fichier sélectionné.'
        else:
            file = request.files['file']
            if file.filename == '':
                error = 'Aucun fichier sélectionné.'
            elif file:
                validation_error = validate_excel(file)
                if validation_error:
                    error = validation_error
                else:
                    ldap_error, results = compare_excel_to_ad(file)
                    if ldap_error:
                        error = ldap_error
            else:
                error = 'Erreur lors de l\'upload du fichier.'

        if error:
            flash(error, 'error')
        return render_template('results.html', results=results)

    return render_template('upload.html')

@app.route('/')
def index():
    """Redirige vers la page de téléchargement."""
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from ldap3 import Server, Connection, ALL, LDAPBindError, LDAPSocketOpenError

app = Flask(__name__)
app.config['SECRET_KEY'] = ' Altice_IT_104729'

# Configuration LDAP (à ADAPTER avec vos informations)
app.config['LDAP_HOST'] = 'ldap.example.com'
app.config['LDAP_PORT'] = 389  # Ou 636 si LDAPS
app.config['LDAP_BASE_DN'] = 'dc=example,dc=com'
app.config['LDAP_BIND_USER_DN'] = 'cn=admin,dc=example,dc=com'
app.config['LDAP_BIND_USER_PASSWORD'] = 'password'
app.config['LDAP_USE_SSL'] = False
app.config['LDAP_SEARCH_SCOPE'] = 'SUBTREE'
app.config['LDAP_USER_OBJECT_FILTER'] = '(objectClass=person)' # Optionnel

def compare_excel_to_ad(excel_file):
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
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
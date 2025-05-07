from flask_ldap3_login import LDAP3LoginManager
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from ldap3 import Server, Connection, ALL



app = Flask(__name__)

app.config['SECRET_KEY'] = ' Altice_IT_104729'

# LDAP Configuration 

app.config['LDAP_HOST'] = 'ldap.example.com'  # on remplace avec le nom de notre serveur LDAP 
app.config['LDAP_BASE_DN'] = 'dc=example,dc=com'  # DN de base pour la recherche
app.config['LDAP_USER_DN'] = 'ou=users,dc=example,dc=com'  # DN de l'unité organisationnelle des utilisateurs
app.config['LDAP_GROUP_DN'] = 'ou=groups,dc=example,dc=com'  # DN de l'unité organisationnelle des groupes
app.config['LDAP_USER_RDN_ATTR'] = 'uid'  # Attribut RDN pour les utilisateurs (ex: uid, cn, etc.)
app.config['LDAP_GROUP_RDN_ATTR'] = 'cn'  # Attribut RDN pour les groupes (ex: cn, ou, etc.)
app.config['LDAP_USER_LOGIN_ATTR'] = 'uid'  # Attribut utilisé pour l'authentification (ex: uid, cn, etc.)
app.config['LDAP_BIND_USER_DN'] = 'cn=admin,dc=example,dc=com'  # DN de l'utilisateur qui a le droit de se connecter
app.config['LDAP_BIND_USER_PASSWORD'] = 'password'  # Mot de passe de l'utilisateur qui a le droit de se connecter
app.config['LDAP_USE_SSL'] = False  # Utiliser SSL ou non
app.config['LDAP_USE_TLS'] = False  # Utiliser TLS ou non
app.config['LDAP_READ_ONLY'] = True  # Si True, l'utilisateur ne peut pas modifier les données LDAP
app.config['LDAP_SEARCH_SCOPE'] = 'SUBTREE'  # Portée de la recherche (BASE, ONELEVEL, SUBTREE)
app.config['LDAP_USER_OBJECT_FILTER'] = '(objectClass=person)'  # Filtre pour les utilisateurs
app.config['LDAP_GROUP_OBJECT_FILTER'] = '(objectClass=groupOfNames)'  # Filtre pour les groupes
app.config['LDAP_USER_GROUP_FILTER'] = '(memberUid={})'  # Filtre pour les groupes d'utilisateurs
app.config['LDAP_GROUP_USER_FILTER'] = '(member={})'  # Filtre pour les utilisateurs de groupes
app.config['LDAP_USER_GROUPS'] = True  # Si True, l'utilisateur peut être membre de plusieurs groupes
app.config['LDAP_GROUPS'] = True  # Si True, les groupes sont activés
app.config['LDAP_USERS'] = True  # Si True, les utilisateurs sont activés

# initialisation de LDAP3LoginManager 


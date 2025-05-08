# SOC_Automation
Coding project made for the SOC team I was part of during my internship with Altice Dominicana

# Comparaison de la liste Excel des nouveaux arrivants avec l'Active Directory (AD)

## Description du Projet

Ce projet est une application desktop autonome conçue pour automatiser la tâche de vérification et de comparaison d'une liste de nouveaux arrivants (fournie sous format Excel) avec les utilisateurs présents dans l'Active Directory de l'entreprise. L'application permet à l'équipe de gagner du temps et de réduire les erreurs en automatisant ce processus manuel.

## Fonctionnement

L'application fonctionne en suivant les étapes suivantes :

1.  **Sélection du fichier Excel :** L'utilisateur sélectionne un fichier Excel contenant une liste de noms de nouveaux arrivants. L'application s'attend à ce que ce fichier contienne une colonne nommée "Nom Complet" avec les noms à vérifier.

2.  **Lecture du fichier Excel :** Une fois le fichier sélectionné, l'application lit le contenu de la colonne "Nom Complet" à l'aide de la librairie `pandas`.

3.  **Connexion à l'Active Directory :** L'application se connecte au serveur Active Directory de l'entreprise en utilisant les informations de configuration LDAP (nom du serveur, port, identifiants de liaison).

4.  **Recherche dans l'AD :** Pour chaque nom extrait de la liste Excel, l'application effectue une recherche dans l'Active Directory en utilisant le nom complet comme critère de recherche (en recherchant une correspondance dans l'attribut `cn` - Common Name).

5.  **Affichage des résultats :** Les résultats de la comparaison sont affichés dans une zone de texte au sein de l'application. Pour chaque nom de la liste Excel, l'application indique s'il a été trouvé ou non dans l'Active Directory. Si une correspondance est trouvée, le nom commun (`cn`) de l'utilisateur AD est affiché. En cas d'erreur lors de la recherche pour un nom spécifique ou lors de la connexion à l'AD, un message d'erreur est également affiché.

## Prérequis

Pour exécuter cette application, les prérequis suivants doivent être satisfaits :

* **Python 3** doit être installé sur le système.
* Les librairies Python suivantes doivent être installées (vous pouvez les installer en utilisant `pip install pandas python-ldap` dans votre terminal) :
    * `pandas` : Pour la lecture et la manipulation des fichiers Excel.
    * `python-ldap` (`ldap3`) : Pour la communication avec le serveur Active Directory via le protocole LDAP.

## Installation et Exécution

1.  **Téléchargez le code source** de l'application (si fourni sous forme de fichiers `.py`).
2.  **Installez les dépendances** en exécutant la commande :
    ```bash
    pip install pandas ldap3
    ```
3.  **Modifiez la configuration LDAP** directement dans le fichier Python (`compare_app.py`) avec les informations spécifiques de votre environnement Active Directory :
    ```python
    LDAP_HOST = 'ldap.example.com'        # Remplacez par l'adresse de votre serveur LDAP
    LDAP_PORT = 389                        # Port LDAP (389 pour LDAP, 636 pour LDAPS)
    LDAP_BASE_DN = 'dc=example,dc=com'    # DN de base pour la recherche
    LDAP_BIND_USER_DN = 'cn=admin,dc=example,dc=com' # DN de l'utilisateur avec les droits de recherche
    LDAP_BIND_USER_PASSWORD = 'password'    # Mot de passe de l'utilisateur de liaison
    LDAP_USE_SSL = False                   # True si vous utilisez LDAPS
    ```
    **Important :** Assurez-vous d'utiliser un compte avec les droits de lecture suffisants dans l'Active Directory pour effectuer les recherches. Évitez d'utiliser des comptes administrateurs si possible et limitez les permissions au strict nécessaire.

4.  **Exécutez l'application** en lançant le script Python principal (par exemple, `compare_app.py`) depuis votre terminal :
    ```bash
    python compare_app.py
    ```
    Une fenêtre graphique s'ouvrira.

## Utilisation

1.  Dans la fenêtre de l'application, cliquez sur le bouton "**Parcourir**" pour sélectionner le fichier Excel contenant la liste des nouveaux arrivants.
2.  Une fois le fichier sélectionné, cliquez sur le bouton "**Lancer la Comparaison**".
3.  Les résultats de la comparaison s'afficheront dans la zone de texte sous le bouton. Pour chaque nom de la liste Excel, vous verrez s'il a été trouvé ou non dans l'Active Directory. Les éventuelles erreurs de connexion ou de recherche seront également affichées.

## Packaging (pour une distribution facile)

Pour distribuer l'application à votre équipe sans qu'ils aient besoin d'installer Python ou des librairies, vous pouvez "packager" l'application en un exécutable unique à l'aide d'outils comme **PyInstaller**.

1.  **Installez PyInstaller :**
    ```bash
    pip install pyinstaller
    ```
2.  **Créez l'exécutable :**
    ```bash
    pyinstaller --onefile compare_app.py
    ```
    L'exécutable sera créé dans le dossier `dist`. Vous pouvez partager ce fichier avec votre équipe.

## Notes et Améliorations Potentielles

* **Gestion des erreurs :** L'application fournit une gestion basique des erreurs de connexion LDAP, de lecture de fichier et de recherche. Des améliorations pourraient être apportées pour une gestion plus détaillée et une journalisation.
* **Interface utilisateur :** L'interface utilisateur actuelle est simple (Tkinter). Des librairies GUI plus avancées comme PyQt ou Kivy pourraient être utilisées pour une interface plus riche.
* **Configuration externe :** Pour une meilleure gestion et sécurité, les informations de configuration LDAP pourraient être déplacées vers un fichier de configuration externe (par exemple, un fichier `.ini` ou `.json`).
* **Options de recherche :** Actuellement, la recherche s'effectue uniquement sur le nom complet (`cn`). Des options pourraient être ajoutées pour rechercher sur d'autres attributs (nom de famille, prénom, etc.) et pour gérer des correspondances partielles ou multiples.
* **Export des résultats :** La possibilité d'exporter les résultats de la comparaison dans un fichier (CSV, Excel) pourrait être utile.

## Contributeurs

mpgamer75

## Licence

Licence MIT
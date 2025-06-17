# Altice File Comparator - Comparateur de Fichiers

## 📋 Description

Application web pour comparer des fichiers CSV, Excel et XLS. Développée pour l'équipe IT d'Altice, cette application permet de :

- **Comparer deux fichiers** (référence vs fichier à comparer)
- **Détecter les différences** au niveau des cellules, lignes et colonnes
- **Générer des rapports** détaillés en format JSON ou TXT
- **Visualiser les résultats** avec des graphiques interactifs
- **Valider les fichiers** avant comparaison

## 🏗️ Architecture

- **Backend**: FastAPI (Python) avec pandas pour le traitement des données
- **Frontend**: Next.js 15 avec React 19 et Tailwind CSS
- **Base de données**: SQLite (pour future utilisation)
- **Logs**: Système de logging intégré

## 🚀 Installation et Démarrage

### Prérequis

- Python 3.12+
- Node.js 18+
- npm ou yarn

### Installation Rapide

1. **Cloner le projet**
```bash
git clone <repository-url>
cd SOC_Automation
```

2. **Installer les dépendances**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

3. **Démarrer en mode production**
```bash
# Depuis la racine du projet
python start_production.py
```

### Démarrage Manuel

#### Backend
```bash
cd backend
python main.py
```
Le serveur backend sera disponible sur `http://localhost:8000`

#### Frontend
```bash
cd frontend
npm run dev
```
L'interface sera disponible sur `http://localhost:3000`

## 📁 Structure du Projet

```
SOC_Automation/
├── backend/
│   ├── main.py                 # Serveur FastAPI principal
│   ├── file_comparator.py      # Logique de comparaison
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Dépendances Python
│   └── app.log               # Fichier de logs
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx      # Page principale
│   │   │   ├── layout.tsx    # Layout de l'application
│   │   │   └── globals.css   # Styles globaux
│   │   └── components/
│   │       └── FileComparatorDashboard.tsx  # Composant principal
│   ├── package.json          # Dépendances Node.js
│   └── next.config.js        # Configuration Next.js
├── start_production.py       # Script de démarrage production
└── README.md                # Ce fichier
```

## 🔧 Configuration

### Variables d'Environnement

Créer un fichier `.env` dans le dossier `backend/` :

```env
# Configuration du serveur
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Configuration CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Configuration des fichiers
MAX_FILE_SIZE=10485760  # 10MB
SUPPORTED_FORMATS=.csv,.xlsx,.xls

# Configuration de sécurité
SECRET_KEY=your-secret-key-change-in-production

# Configuration des logs
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### Configuration Frontend

Créer un fichier `.env.local` dans le dossier `frontend/` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 Fonctionnalités

### Comparaison de Fichiers

1. **Upload de fichiers** : Interface drag & drop pour sélectionner les fichiers
2. **Validation** : Vérification automatique du format et de la taille
3. **Comparaison** : Analyse détaillée des différences
4. **Rapports** : Génération de rapports en JSON ou TXT
5. **Visualisation** : Graphiques des différences trouvées

### Types de Différences Détectées

- **Celdas modificadas** : Valeurs modifiées dans les cellules
- **Filas agregadas/eliminadas** : Lignes ajoutées ou supprimées
- **Columnas agregadas/eliminadas** : Colonnes ajoutées ou supprimées
- **Diferencias estructurales** : Différences dans la structure

### Formats Supportés

- **CSV** : Fichiers CSV avec encodage UTF-8, Latin-1, CP1252
- **Excel** : Fichiers .xlsx et .xls
- **Taille maximale** : 10MB par fichier (configurable)

## 🔌 API Endpoints

### GET /
- **Description** : Vérification du statut de l'API
- **Réponse** : Informations sur l'API et formats supportés

### GET /health
- **Description** : Endpoint de santé pour le monitoring
- **Réponse** : Statut du service

### POST /compare
- **Description** : Comparaison de deux fichiers
- **Paramètres** : `file1` (référence), `file2` (à comparer)
- **Réponse** : Résultat détaillé de la comparaison

### POST /validate-file
- **Description** : Validation d'un fichier
- **Paramètres** : `file` (fichier à valider)
- **Réponse** : Informations sur le fichier

## 📈 Monitoring et Logs

### Logs Backend

Les logs sont automatiquement générés dans `backend/app.log` avec les niveaux :
- **INFO** : Opérations normales
- **ERROR** : Erreurs de traitement
- **DEBUG** : Informations détaillées (si DEBUG=True)

### Monitoring

- **Health Check** : `GET /health`
- **Documentation API** : `http://localhost:8000/docs`
- **Logs en temps réel** : Affichés dans la console

## 🚀 Déploiement en Production

### 1. Préparation

```bash
# Build du frontend
cd frontend
npm run build

# Test du backend
cd ../backend
python -m pytest tests/
```

### 2. Configuration Production

```env
# .env production
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=your-very-secure-secret-key
ALLOWED_ORIGINS=https://your-domain.com
```

### 3. Démarrage Production

```bash
# Utiliser le script de production
python start_production.py

# Ou démarrer manuellement
cd backend && python main.py &
cd frontend && npm start &
```

### 4. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 Sécurité

### Mesures Implémentées

- **Validation des fichiers** : Type et taille
- **CORS configuré** : Origines autorisées
- **Gestion d'erreurs** : Messages d'erreur sécurisés
- **Logs sécurisés** : Pas d'informations sensibles

### Recommandations Production

- **HTTPS** : Utiliser un certificat SSL
- **Firewall** : Restreindre l'accès aux ports
- **Monitoring** : Surveiller les logs et performances
- **Backup** : Sauvegarder les données importantes

## 🐛 Dépannage

### Problèmes Courants

1. **Port déjà utilisé**
   ```bash
   # Vérifier les ports
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :3000
   ```

2. **Dépendances manquantes**
   ```bash
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   npm install
   ```

3. **Erreur CORS**
   - Vérifier `ALLOWED_ORIGINS` dans la configuration
   - S'assurer que le frontend et backend sont sur les bons ports

4. **Fichier trop volumineux**
   - Augmenter `MAX_FILE_SIZE` dans la configuration
   - Ou réduire la taille du fichier

### Logs de Débogage

```bash
# Activer les logs détaillés
export LOG_LEVEL=DEBUG
python main.py
```

## 📞 Support

Pour toute question ou problème :

1. **Vérifier les logs** : `backend/app.log`
2. **Consulter la documentation API** : `http://localhost:8000/docs`
3. **Tester les endpoints** : Utiliser les outils de test

## 🔄 Mise à Jour

### Mise à Jour du Code

```bash
git pull origin main
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### Mise à Jour des Dépendances

```bash
# Backend
pip list --outdated
pip install -U package-name

# Frontend
npm outdated
npm update
```

---

**Version** : 1.0.0  
**Dernière mise à jour** : 2024  
**Équipe** : IT Altice 
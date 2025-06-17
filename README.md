# 🎯 Altice File Comparator

Une application web moderne pour comparer des fichiers CSV, Excel et XLS de manière intelligente et visuelle.

## 🚀 Fonctionnalités

- **Comparaison intelligente** : Détecte les différences entre fichiers CSV, XLSX et XLS
- **Interface moderne** : Interface utilisateur intuitive avec drag & drop
- **Visualisations** : Graphiques interactifs pour analyser les différences
- **Rapports détaillés** : Statistiques complètes et listes de différences
- **Performance** : Traitement rapide même pour de gros fichiers
- **Multi-format** : Support complet pour CSV, Excel et XLS

## 🏗️ Architecture

- **Backend** : FastAPI (Python) avec pandas pour le traitement des données
- **Frontend** : Next.js (React) avec TypeScript et Tailwind CSS
- **Graphiques** : Recharts pour les visualisations
- **Configuration** : Système de configuration flexible avec variables d'environnement

## 📋 Prérequis

- Python 3.8+
- Node.js 16+
- npm ou yarn

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd altice-project/SOC_Automation
```

### 2. Installer les dépendances du backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Installer les dépendances du frontend
```bash
cd ../frontend
npm install
```

## 🚀 Démarrage rapide

### Option 1 : Utiliser le script batch (Windows)
Double-cliquez sur `demarrer_application.bat` et suivez les instructions.

### Option 2 : Utiliser les scripts Python

#### Mode développement
```bash
python start_dev.py
```

#### Mode production
```bash
python start_production.py
```

### Option 3 : Démarrage manuel

#### Backend
```bash
cd backend
python main.py
```

#### Frontend
```bash
cd frontend
npm run dev
```

## 🌐 Accès à l'application

- **Interface web** : http://localhost:3000
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` dans le dossier `backend` avec les paramètres suivants :

```env
# Configuration du serveur
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Configuration CORS
FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Configuration des fichiers
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=csv,xlsx,xls

# Configuration de sécurité
SECRET_KEY=your-secret-key-here

# Configuration des logs
LOG_LEVEL=INFO
LOG_FILE=app.log

# Configuration de l'environnement
ENV=production
```

## 📊 Fonctionnalités de comparaison

### Types de différences détectées

1. **Différences structurelles**
   - Nombre de colonnes différent
   - Colonnes manquantes ou ajoutées
   - Noms de colonnes différents

2. **Différences de contenu**
   - Celdas modifiées
   - Filas ajoutées ou supprimées
   - Valeurs différentes dans les mêmes positions

### Statistiques fournies

- Nombre total de différences
- Répartition par type de différence
- Temps de traitement
- Métadonnées des fichiers

## 🎨 Interface utilisateur

### Fonctionnalités principales

- **Drag & Drop** : Glissez-déposez vos fichiers directement
- **Validation en temps réel** : Vérification automatique des formats
- **Graphiques interactifs** : Visualisations des différences
- **Tableau détaillé** : Liste complète des différences
- **Design responsive** : Compatible mobile et desktop

### Composants visuels

- **Graphiques en barres** : Comparaison de structure
- **Graphiques circulaires** : Répartition des différences
- **Cartes de statistiques** : Résumé rapide
- **Tableaux détaillés** : Analyse approfondie

## 🔧 Développement

### Structure du projet

```
SOC_Automation/
├── backend/
│   ├── main.py              # Serveur FastAPI
│   ├── file_comparator.py   # Logique de comparaison
│   ├── config.py            # Configuration
│   └── requirements.txt     # Dépendances Python
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   └── components/
│   │       └── FileComparatorDashboard.tsx
│   └── package.json
├── start_dev.py             # Script de développement
├── start_production.py      # Script de production
└── demarrer_application.bat # Lanceur Windows
```

### Scripts disponibles

- `start_dev.py` : Mode développement avec hot reload
- `start_production.py` : Mode production optimisé
- `demarrer_application.bat` : Interface graphique Windows

## 🐛 Dépannage

### Problèmes courants

1. **Port déjà utilisé**
   - Changez le port dans le fichier `.env`
   - Ou arrêtez les processus utilisant les ports 3000/8000

2. **Dépendances manquantes**
   - Vérifiez que Python et Node.js sont installés
   - Relancez l'installation des dépendances

3. **Erreurs CORS**
   - Vérifiez la configuration `FRONTEND_URL` dans `.env`
   - Assurez-vous que les URLs correspondent

4. **Fichiers trop volumineux**
   - Augmentez `MAX_FILE_SIZE` dans `.env`
   - Ou réduisez la taille des fichiers

### Logs

Les logs sont disponibles dans :
- **Backend** : `backend/app.log`
- **Frontend** : Console du navigateur

## 📈 Performance

### Optimisations

- Traitement par chunks pour les gros fichiers
- Limitation des différences affichées (100 max)
- Conversion en string pour éviter les problèmes de types
- Support multi-encodage pour les CSV

### Limites

- Taille maximale de fichier : 10MB par défaut
- Nombre de différences affichées : 100 max
- Formats supportés : CSV, XLSX, XLS

## 🔒 Sécurité

- Validation des types de fichiers
- Limitation de la taille des fichiers
- Configuration CORS sécurisée
- Gestion des erreurs robuste

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation API sur http://localhost:8000/docs
- Vérifiez les logs dans `backend/app.log`

---

**🎯 Altice File Comparator** - Comparaison intelligente de fichiers

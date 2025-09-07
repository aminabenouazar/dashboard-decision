# 📊 Dashboard d’Aide à la Décision – Chocodor

## 🚀 Description du projet
Ce projet consiste à développer un **tableau de bord interactif** permettant l’analyse et la visualisation des ventes de chocolat pour **Chocodor**, un magasin spécialisé.  

🎯 Objectifs :
- Suivre les **tendances de ventes** 📈  
- Identifier les **produits les plus performants** 🍫  
- Anticiper les **préférences des clients** et la **demande future** 🔮  

💡 Le projet combine **visualisation interactive**, **prétraitement des données** et **analyse prédictive** afin de soutenir la prise de décision.

---

## 📂 Structure du projet
code3/
│── modele/ # Scripts & modèles ML (.pkl, .ipynb, .csv)

│── static/ # Fichiers statiques (images, CSS, JS)

│── templates/ # Templates HTML pour l’interface

│── api.py # Backend FastAPI

│── visualisation.py # Scripts de visualisation

│── chocolate_sales.csv # Dataset (⚠️ à télécharger depuis Google Drive)


---

## ⚙️ Installation & Lancement

### 1️⃣ Créer un environnement virtuel
```bash
python -m venv venv
Sous Windows :

bash
Copy code
venv\Scripts\activate
Sous Linux / Mac :

bash
Copy code
source venv/bin/activate
2️⃣ Installer les dépendances
bash
Copy code
pip install -r requirements.txt
3️⃣ Lancer le serveur FastAPI
bash
Copy code
uvicorn api:app --reload
Le dashboard sera accessible sur 👉 http://127.0.0.1:8000/

📂 Datasets & Modèles
⚠️ Pour des raisons de taille, les datasets et modèles ne sont pas stockés sur GitHub.
👉 Téléchargez-les depuis Google Drive :

📥 chocolate_sales.csv :https://drive.google.com/file/d/1NGeoTyoHZSN6BGnkDacCxkmx12mbPBp7/view?usp=sharing

📥 model_regression.pkl : https://drive.google.com/file/d/1yFJa1A-kRQQFnf8JChvJwET2F2xdzlEx/view?usp=sharing

📥 label_encoder.pkl :  https://drive.google.com/file/d/1Kp49wTDz7kHtPu2-bWPZiz4WQBQcR5k7/view

📌 Emplacements des fichiers
bash
Copy code
/modele/chocolate_sales.csv
/modele/modele/model_regression.pkl
/modele/modele/label_encoder.pkl
🏪 Contexte – Chocodor
Chocodor est un magasin de vente de chocolat.

Le besoin exprimé par le client :

Manque de visibilité sur les produits les plus vendus

Difficulté dans la planification des achats et de la production

✅ Solutions apportées :

Prétraitement et nettoyage des données de 4 années de ventes

Conception d’un tableau de bord en temps réel pour visualiser les tendances

Développement d’un modèle prédictif afin d’anticiper les chocolats les plus demandés

✨ Auteur
👩‍💻 Amina Benouazar
Étudiante en Ingénierie Digitale pour la Finance – ENSIAS
Passionnée par la Data Science & la Finance 📊💡



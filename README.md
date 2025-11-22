# 🧠 Profile Extractor NLP – Streamlit App

Cette application permet d’extraire automatiquement un **profil structuré** à partir d’un texte libre.  
Elle utilise des techniques de **Traitement Automatique du Langage (NLP)** avec **spaCy**, des **regex intelligentes**, et une interface web moderne construite avec **Streamlit**.

---

## 🚀 Fonctionnalités

### ✔️ Extraction automatique des informations suivantes :
- **Nom complet**
- **Date de naissance** (formats variés : `05/08/2002`, `5 août 2002`, `5 August 2002`…)
- **Université / école**
- **Ville / lieu de résidence**
- **E-mail**
- **Numéro de téléphone**

### ✔️ Normalisation automatique :
- Nettoyage du texte (accents, espaces…)
- Uniformisation des dates → format `DD-MM-YYYY`

### ✔️ Modèle NLP utilisé
- `spaCy - fr_core_news_lg` (meilleure précision : NER, segmentation…)
- Couplé avec des **regex personnalisées** pour augmenter la précision (université, localisation, nom…).

### ✔️ Interface utilisateur (UI)
- Saisie d’un texte libre
- Bouton de génération de profil
- Affichage élégant du profil structuré
- **Avatar IA généré automatiquement** (via *randomuser.me*)

---

## 🏗️ Architecture du projet

📦 NLP_Profile_Extractor
┣ 📜 appNLP.py
┣ 📜 requirements.txt
┣ 📜 README.md
┗ 📁 assets (optionnel)

---

## 🛠️ Installation

### 1️⃣ Cloner le projet

git clone https://github.com/username/your-repo.git
cd your-repo

### 2️⃣ Créer un environnement

conda create -n nlp_env python=3.11
conda activate nlp_env

### 3️⃣ Installer les dépendances

pip install -r requirements.txt

-->spaCy installera automatiquement le modèle fr_core_news_lg grâce au lien dans requirements.txt.

### ▶️ Lancement de l’application

streamlit run appNLP.py

### 🧩 Exemple de texte à tester
![Text](Assets/text.png)

Resultat obtenu:

![Profil](Assets/profile.png)

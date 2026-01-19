# ⚖️ Legal-RAG : Assistant Code du Travail Marocain

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![AI](https://img.shields.io/badge/AI-RAG-orange)
![Local](https://img.shields.io/badge/Privacy-100%25_Local-green)

**Legal-RAG** est une intelligence artificielle conversationnelle spécialisée dans le **Droit du Travail Marocain**. 

Contrairement aux LLMs génériques (ChatGPT, Gemini) qui peuvent "halluciner" des lois, ce système utilise une architecture **RAG (Retrieval-Augmented Generation)**. Il interroge une base de données vectorielle contenant le Code du Travail officiel pour fournir des réponses **sourcées, précises et juridiquement fiables** en Français et en Arabe.

---

## 🚀 Fonctionnalités Clés

* **🔍 Zéro Hallucination :** L'IA répond *uniquement* sur la base des articles de loi fournis. Si elle ne sait pas, elle le dit.
* **🌍 Multilingue & RTL :** Support natif de l'Arabe (avec affichage de droite à gauche) et du Français.
* **📚 Citations Exactes :** Chaque réponse mentionne l'article de référence (ex: *Source : Article 152*).
* **✂️ Semantic Chunking :** Découpage intelligent du texte par "Article" (et non par page) pour préserver le sens juridique.
* **🔒 100% Local :** Fonctionne entièrement sur votre machine avec **Ollama** et **ChromaDB**. Aucune donnée ne part dans le cloud.

---

## 🛠️ Architecture Technique

Ce projet repose sur une stack Deep Learning moderne :

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **LLM** | `Mistral 7B` (via Ollama) | Génération de réponse et compréhension du langage naturel. |
| **Embeddings** | `multilingual-MiniLM-L12-v2` | Transformation du texte juridique en vecteurs mathématiques. |
| **Vector Store** | `ChromaDB` | Base de données locale pour la recherche de similarité. |
| **Orchestration** | `LangChain` | Gestion du pipeline (Prompting, Retrieval). |
| **Interface** | `Streamlit` | Interface Web utilisateur. |

---

## 📂 Structure du Projet

```text
Legal_RAG/
├── d2c1f...code_travail.pdf   # Le document source (Code du Travail)
├── ingest.py                  # Étape 1 : Nettoyage & Découpage (Chunking)
├── vectorize.py               # Étape 2 : Création de la base vectorielle (Embedding)
├── app.py                     # Étape 3 : L'application Chatbot (Streamlit)
├── requirements.txt           # Liste des dépendances Python
├── data_clean.json            # Données nettoyées (généré par ingest.py)
└── chroma_db/                 # Base de données vectorielle (généré par vectorize.py)
```
## 📦 Installation & Démarrage
Suivez ces étapes pour lancer le projet sur votre machine.
1. Prérequis

- Python 3.9+ installé.
- Ollama installé et lancé (Télécharger sur ollama.com).

2. Cloner le projet
```bash
git clone https://github.com/wijdanelbakhouchi/Projet_Legal_RAG.git
cd Legal_RAG
```
3. Créer l'environnement virtuel
```bash
python -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate
```
4. Installer les dépendances

```bash
pip install -r requirements.txt
```
5. Configurer le modèle LLM
Assurez-vous qu'Ollama est lancé, puis téléchargez le modèle Mistral (optimisé pour le multilingue) :
```bash
ollama pull mistral
```
## ⚙️ Initialisation des Données (Pipeline)
Avant de lancer l'application, vous devez traiter le PDF et créer la base de données.
**Étape A : Nettoyage et Découpage** Ce script lit le PDF, nettoie les en-têtes et sépare les articles juridiques.
```bash
python ingest.py
```
Résultat : Création du fichier data_clean.json.
**Étape B : Vectorisation (Indexation)** Ce script transforme les articles en vecteurs et remplit ChromaDB.
```bash
python vectorize.py
```
Résultat : Création du dossier chroma_db/.
## ▶️ Lancer l'Application
Une fois la base de données prête, lancez l'interface de chat :
```bash
streamlit run app.py
```
L'application s'ouvrira automatiquement dans votre navigateur (généralement http://localhost:8501).

## 🧪 Exemples de Questions

Essayez de piéger l'IA ou de poser des questions complexes :
### En Français
- "Quelle est la durée du congé de maternité ?"
- "Quelles sont les indemnités en cas de licenciement abusif ?"
- "Quelle est la durée de la période d'essai pour un cadre ?"
### En Arabe (Standard)
- "ما هي مدة العطلة السنوية المؤدى عنها؟" (Quelle est la durée du congé annuel payé ?)
- "متى يعتبر الطرد تعسفياً؟" (Quand le licenciement est-il abusif ?)
- "ما هو السن القانوني للتشغيل؟" (Quel est l'âge légal de travail ?)

##👤 Auteurs
Projet réalisé dans le cadre académique (Master Intelligent Processing Systems / Deep Learning).
**Par :**
- ELBAKHOUCHI Wijdane
- BENZRIOUAL Amine
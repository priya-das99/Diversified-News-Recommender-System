# Diversified News Recommendation System

A sophisticated news recommendation system that provides personalized news recommendations while maintaining content diversity and preventing echo chambers.

## 📑 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Technical Architecture](#-technical-architecture)
- [Installation](#-installation)
- [Running Locally](#-running-locally)
- [Project Structure](#-project-structure)
- [Implementation Details](#-implementation-details)
- [Credits](#-credits)

## 🎯 Overview

This news recommendation system uses a hybrid approach combining collaborative filtering and content-based recommendations to provide users with personalized news content while ensuring diversity in the recommendations. The system employs Skip-Gram (a word2vec model) embeddings for article representation and implements an innovative diversity-aware reranking algorithm.

## ✨ Features

- **Personalized Recommendations**: Uses hybrid recommendation approach (Collaborative + Content-based)
- **Diversity Enhancement**: Implements diversity-aware reranking algorithm
- **Cold Start Handling**: Special handling for new users and articles

- **Modern Web Interface**: Responsive UI built with TailwindCSS
- **Scalable Architecture**: Optimized for handling large datasets

## 🏗 Technical Architecture

### Backend Stack
- Python 3.8+
- Flask (Web Framework)
- NumPy & Pandas (Data Processing)
- Scikit-learn (Machine Learning)
- FAISS (Similarity Search)
- skip-gram (Text Embeddings)

### Frontend Stack
- HTML5/CSS3
- JavaScript
- TailwindCSS
- PostCSS

## 📦 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/priya-das99/Diversified-News-Recommender-System.git
cd Diversified-News-Recommender-System
```

2. **Set Up Python Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Install Node.js Dependencies**
```bash
npm install
```

4. **Build CSS**
```bash
npm run build:css
```

## 🚀 Running Locally

1. **Start the Flask Backend**
```bash
python backend/app.py
```

2. **Watch CSS Changes (Development)**
```bash
npm run watch:css
```

3. Access the application at `http://localhost:5000`

## 📁 Project Structure

```
project/
├── backend/               # Server-side code
│   ├── app.py            # Flask application and routes
│   ├── database.py       # Database and data loading functions
│   ├── collaborative.py  # Collaborative filtering algorithm
│   ├── content_based.py  # Content-based filtering
│   ├── diversity_ReRank.py # Diversity reranking algorithm
│   ├── hybrid.py         # Hybrid recommendation system
│   └── utils.py          # Utility functions
├── data/                 # Dataset and processing scripts
├── frontend/            
│   ├── static/          # Static assets
│   │   ├── css/         # Stylesheets
│   │   └── js/          # JavaScript files
│   ├── templates/       # HTML templates
│   ├── package.json     # Frontend dependencies
│   └── postcss.config.js # PostCSS configuration
├── package.json         # Project dependencies
└── requirements.txt     # Python dependencies
```

## 🛠 Implementation Details

### Recommendation System Components

1. **Collaborative Filtering** (`collaborative.py`)
   - User-based similarity calculations
   - Item-based similarity calculations 
   - Similar user identification using cosine similarity  using FAISS for faster search 

2. **Content-Based Filtering** (`content_based.py`)
   - Skip-gram embeddings for article representation
   - Article similarity calculations
   - Similar article recommendation

3. **Diversity Enhancement** (`diversity_ReRank.py`)
   - Diversity-aware reranking algorithm
   - Category coverage optimization
   - Echo chamber prevention

4. **Hybrid Recommendations** (`hybrid.py`)
   - Combines collaborative and content-based approaches
   - Weighted score aggregation
   - Adaptive recommendation strategy

## 👥 Credits

This project was developed as part of a minor project by:

**Team Members:**

- [Priya Das](https://github.com/priya-das99) - Research and implementation(Code Integration)
- [Subrojyoti Paul](https://github.com/Subrojyoti) - Algorithm Design and implementation


**Supervisors:**
- [Dr. Tribikram Pradhan - Project Guide]
- [Computer science and Engineering] - [Tezpur University]



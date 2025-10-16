# IntelliDoc: KI-gestützte Dokumentenintelligenz-Plattform (Deutsch)

##  Projektbeschreibung

IntelliDoc ist eine Ende-zu-Ende-Plattform für KI-gestützte Dokumentintelligenz. Benutzer können Dokumente hochladen, automatisch analysieren lassen und Fragen zu deren Inhalt stellen. Die Anwendung nutzt moderne ML-Verfahren für Textextraktion, Klassifizierung, Zusammenfassung und semantische Suche.

##  Hauptfunktionen

###  Dokumentenverarbeitung
- **Multi-Format-Unterstützung**: PDF, DOCX, TXT, JPG, PNG
- **Automatische Textextraktion**: OCR für Bilder, nativer Text für Dokumente
- **KI-Klassifizierung**: Automatische Kategorisierung von Dokumenten
- **Zusammenfassung**: Abstraktive/extraktive Zusammenfassungen

###  KI-gestützte Analyse
- **Dokumenten-Q&A**: Stellen Sie Fragen zu Ihren Dokumenten
- **Semantische Suche**: Bedeutungsgestützte Suche über alle Dokumente
- **Vektorbasierte Ähnlichkeitssuche**: ChromaDB-basiert
- **Mehrsprachigkeit**: Optionale Übersetzung

###  Analytics & Dashboard
- **Benutzer-Dashboard**: Übersicht über Dokumente und Kennzahlen
- **Kategorie-Verteilung**: Visualisierung der Dokumenttypen
- **Verarbeitungsmetriken**: Status- und Volumen-Tracking
- **Interaktive Diagramme**: Plotly

###  Sicherheit & Benutzerverwaltung
- **JWT-Authentifizierung**
- **Benutzerisolation**
- **Passwort-Hashing**

##  Technologie-Stack

### Backend
- **FastAPI**, **SQLAlchemy**, **SQLite/PostgreSQL**, optional **Redis/Celery**

### KI & ML
- **Transformers**, **PyTorch**, **Sentence Transformers**, **ChromaDB**

### Dokumentenverarbeitung
- **PyPDF2**, **python-docx**, **Tesseract OCR**, **OpenCV**, **Pillow**

### Frontend
- **Streamlit**, **Plotly**, **Pandas**

##  Systemanforderungen

- **Python**: 3.13 (oder 3.12)
- **OS**: Windows, macOS, Linux
- **RAM**: 4GB+ (8GB+ empfohlen für lokale Modelle)
- **Speicher**: 2GB frei
- **Tesseract OCR** (für Bild-Texterkennung)

##  Installation

### Abhängigkeiten installieren (Einzeldatei)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

Hinweise:
- Die Versionen sind Python-3.13-kompatibel (vorbereitete Wheels für transformers/tokenizers/torch).
- Für die Installation ist unter diesen Versionen keine Rust-Toolchain erforderlich.

##  Starten

### Schnellstart
```bash
python run_app.py
```

### Manueller Start

#### Backend starten
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend starten (in einem neuen Terminal)
```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```

##  Zugriff

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API-Dokumentation**: http://localhost:8000/docs
- **Alternative Doku**: http://localhost:8000/redoc

##  Nutzung

### 1. Registrierung
1. Öffnen Sie http://localhost:8501
2. Wechseln Sie zum Tab „Register“
3. Neues Konto erstellen

### 2. Dokumente hochladen
1. Anmelden
2. „Documents“ → „Upload“
3. Datei wählen (PDF, DOCX, TXT, JPG, PNG)
4. Optional Kategorie wählen
5. „Upload Document“ klicken

### 3. Analyse
- Automatische Analyse beim Upload
- Fragen über Q&A stellen
- Semantische Suche über alle Dokumente
- Automatische Kategorisierung

### 4. Dashboard
- Übersicht, Statistiken, Verteilungen, letzte Dokumente

### API-Endpunkte (Auszug)
- Auth: `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- Dokumente: `POST /api/documents/upload`, `GET /api/documents/`, `GET /api/documents/{id}`, `POST /api/documents/{id}/query`, `POST /api/documents/search`, `DELETE /api/documents/{id}`
- Analytics: `GET /api/analytics/dashboard`

##  Tests & Entwicklung

### Tests ausführen
```bash
# PowerShell
$env:PYTHONPATH=(Get-Location).Path; pytest -q

# Bash/zsh
PYTHONPATH=$(pwd) pytest -q
```

Leichtgewichtiger Startmodus für lokale Entwicklung (überspringt schwere ML-Initialisierung, nutzt In-Memory-Vektorspeicher):
```bash
# PowerShell
$env:INTELLIDOC_FAST_INIT='1'

# Bash/zsh
export INTELLIDOC_FAST_INIT=1
```

### Projektstruktur
```
intellidoc/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI-Hauptanwendung
│   ├── config.py              # Konfiguration
│   ├── database.py            # Datenbankverbindung
│   ├── models.py              # SQLAlchemy-Modelle
│   ├── schemas.py             # Pydantic-Schemas
│   ├── auth.py                # Authentifizierung
│   ├── crud.py                # Datenbankoperationen
│   ├── api/                   # API-Routen
│   │   ├── auth.py
│   │   ├── documents.py
│   │   └── analytics.py
│   ├── services/              # Geschäftslogik
│   │   ├── document_processor.py
│   │   ├── ai_service.py
│   │   └── vector_store.py
│   └── utils/
│       └── helpers.py
├── frontend/
│   └── streamlit_app.py       # Streamlit-Frontend
├── requirements.txt           # Python-Abhängigkeiten (Einzeldatei)
├── .env                       # Umgebungsvariablen
├── run_app.py                 # Starter
└── README.md                  # Diese Datei
```

### Tooling
- Formatierung: black, isort
- Linting: flake8
- Typprüfung: mypy

### Häufige Probleme
- Falls OCR bei Bildern fehlschlägt, Tesseract installieren und PATH prüfen.
- Bei vorhandener GPU nutzt `torch==2.9.0` CUDA, falls korrekt konfiguriert, sonst CPU.

# IntelliDoc: AI-Powered Document Intelligence Platform

##  Project Description

IntelliDoc is an end-to-end AI-powered document intelligence platform that lets users upload, analyze, and ask questions about documents. It leverages modern ML for text extraction, document classification, summarization, and semantic search.

##  Key Features

###  Document Processing
- **Multi-format support**: PDF, DOCX, TXT, JPG, PNG
- **Automatic text extraction**: OCR for images, native text for documents
- **AI classification**: Automatic document categorization
- **Summarization**: Abstractive/extractive summary generation

###  AI-powered Analysis
- **Document Q&A**: Ask questions about your documents
- **Semantic search**: Search all documents by meaning
- **Vector similarity search**: ChromaDB-backed
- **Multilingual support**: Optional translation

###  Analytics & Dashboard
- **User dashboard**: Overview of documents and stats
- **Category distribution**: Visualizing document types
- **Processing metrics**: Track processing status and volumes
- **Interactive charts**: Plotly

###  Security & User Management
- **JWT authentication**
- **User isolation**
- **Password hashing**

##  Tech Stack

### Backend
- **FastAPI**
- **SQLAlchemy**
- **SQLite/PostgreSQL**
- **(Optional) Redis/Celery**

### AI & ML
- **Transformers** (Hugging Face)
- **PyTorch**
- **Sentence Transformers**
- **ChromaDB**

### Document Processing
- **PyPDF2**, **python-docx**, **Tesseract OCR**, **OpenCV**, **Pillow**

### Frontend
- **Streamlit**, **Plotly**, **Pandas**

##  Requirements

- **Python**: 3.9+
- **OS**: Windows, macOS, Linux
- **RAM**: 4GB+ (8GB+ recommended for local models)
- **Disk**: 2GB free
- **Tesseract OCR** (for image text extraction)

##  Getting Started

### Quickstart
```bash
python run_app.py
```

### Manual Start

#### Start the backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Start the frontend (in a new terminal):
```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```

##  Installation

### Prerequisites
- Python 3.13 (or 3.12)
- Windows, macOS, or Linux
- Optional for image OCR: Tesseract installed and on PATH

### Install dependencies (single file)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

Notes:
- Pins are set to be compatible with Python 3.13 (transformers/tokenizers/torch publish cp313 wheels).
- No Rust is required for installation under these pins.

##  Access

Once started, the following URLs are available:

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Alt Docs**: http://localhost:8000/redoc

##  Usage

### 1. Register
1. Open http://localhost:8501
2. Go to the "Register" tab
3. Create a new account

### 2. Upload Documents
1. Log in
2. Go to "Documents" → "Upload"
3. Choose a file (PDF, DOCX, TXT, JPG, PNG)
4. Optionally choose a category
5. Click "Upload Document"

### 3. Analyze Documents
- Automatic analysis on upload
- Ask questions via Q&A
- Semantic search across all documents
- Auto-categorization

### 4. Dashboard
- Overview of all your documents
- Stats and metrics
- Category distributions
- Recent documents

### Authentication
- `POST /api/auth/register` - Benutzerregistrierung
- `POST /api/auth/login` - Benutzeranmeldung
- `GET /api/auth/me` - Benutzerprofil abrufen

### Documents
- `POST /api/documents/upload` - Dokument hochladen
- `GET /api/documents/` - Alle Dokumente abrufen
- `GET /api/documents/{id}` - Einzelnes Dokument abrufen
- `POST /api/documents/{id}/query` - Dokument befragen
- `POST /api/documents/search` - Semantische Suche
- `DELETE /api/documents/{id}` - Dokument löschen

### Analytics
- `GET /api/analytics/dashboard` - Dashboard-Statistiken

##  Testing & Development

### Run tests
```bash
# PowerShell
$env:PYTHONPATH=(Get-Location).Path; pytest -q

# Bash/zsh
PYTHONPATH=$(pwd) pytest -q
```

You can enable a light startup mode for local development (skips heavy ML downloads and uses in-memory vector store) by exporting:
```bash
# PowerShell
$env:INTELLIDOC_FAST_INIT='1'

# Bash/zsh
export INTELLIDOC_FAST_INIT=1
```

### Project Structure
```
intellidoc/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI-Hauptanwendung
│   ├── config.py              # Konfiguration
│   ├── database.py            # Datenbankverbindung
│   ├── models.py              # SQLAlchemy-Modelle
│   ├── schemas.py             # Pydantic-Schemas
│   ├── auth.py                # Authentifizierung
│   ├── crud.py                # Datenbankoperationen
│   ├── api/                   # API-Routen
│   │   ├── auth.py
│   │   ├── documents.py
│   │   └── analytics.py
│   ├── services/              # Geschäftslogik
│   │   ├── document_processor.py
│   │   ├── ai_service.py
│   │   └── vector_store.py
│   └── utils/
│       └── helpers.py
├── frontend/
│   └── streamlit_app.py       # Streamlit-Frontend
├── requirements.txt           # Python dependencies (single file)
├── .env                       # Environment variables
├── run_app.py                 # Launcher
└── README.md                  # This file

### Tooling
- Formatting: black, isort
- Linting: flake8
- Type checking: mypy

### Common issues
- If OCR fails on images, ensure Tesseract is installed and available on PATH.
- If GPU is available, `torch==2.9.0` will use CUDA when properly configured; otherwise it runs on CPU.
```

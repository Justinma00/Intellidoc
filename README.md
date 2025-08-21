# IntelliDoc: KI-gestützte Dokumentenintelligenz-Plattform

##  Projektbeschreibung

IntelliDoc ist eine vollständige KI-gestützte Dokumentenintelligenz-Plattform, die es Benutzern ermöglicht, Dokumente hochzuladen, zu analysieren und intelligente Fragen zu stellen. Die Anwendung nutzt moderne Machine Learning-Technologien für automatische Textextraktion, Dokumentenklassifizierung, Zusammenfassung und semantische Suche.

##  Hauptfunktionen

###  Dokumentenverarbeitung
- **Multi-Format-Unterstützung**: PDF, DOCX, TXT, JPG, PNG
- **Automatische Textextraktion**: OCR für Bilder, nativer Text für Dokumente
- **KI-Klassifizierung**: Automatische Kategorisierung von Dokumenten
- **Intelligente Zusammenfassung**: Generierung von Dokumentenzusammenfassungen

###  KI-gestützte Analyse
- **Dokumenten-Q&A**: Stellen Sie Fragen zu Ihren Dokumenten
- **Semantische Suche**: Durchsuchen Sie alle Dokumente nach Bedeutung
- **Vektorbasierte Ähnlichkeitssuche**: ChromaDB für erweiterte Suchfunktionen
- **Mehrsprachige Unterstützung**: Übersetzung und Analyse in verschiedenen Sprachen

###  Analytics & Dashboard
- **Benutzer-Dashboard**: Übersicht über alle Dokumente und Statistiken
- **Kategorie-Verteilung**: Visualisierung der Dokumententypen
- **Verarbeitungsmetriken**: Tracking der KI-Verarbeitungsleistung
- **Interaktive Diagramme**: Plotly-basierte Visualisierungen

###  Sicherheit & Benutzererverwaltung
- **JWT-Authentifizierung**: Sichere Benutzeranmeldung
- **Benutzerisolation**: Jeder Benutzer sieht nur seine eigenen Dokumente
- **Passwort-Hashing**: Sichere Speicherung von Benutzerdaten

##  Verwendete Technologien

### Backend
- **FastAPI**: Moderne, schnelle Web-API-Framework
- **SQLAlchemy**: SQL-Datenbank-ORM
- **PostgreSQL/SQLite**: Relationale Datenbank
- **Redis**: Caching und Session-Management
- **Celery**: Asynchrone Aufgabenverarbeitung

### KI & Machine Learning
- **Transformers**: Hugging Face Transformers-Bibliothek
- **PyTorch**: Deep Learning Framework
- **Sentence Transformers**: Für Texteinbettungen
- **ChromaDB**: Vektordatenbank für semantische Suche
- **LangChain**: LLM-Anwendungsframework

### Dokumentenverarbeitung
- **PyPDF2**: PDF-Textextraktion
- **python-docx**: DOCX-Verarbeitung
- **Tesseract OCR**: Optische Zeichenerkennung
- **OpenCV**: Bildverarbeitung
- **Pillow**: Bildmanipulation

### Frontend
- **Streamlit**: Interaktive Web-Anwendung
- **Plotly**: Interaktive Datenvisualisierung
- **Pandas**: Datenanalyse und -manipulation

##  Systemanforderungen

- **Python**: 3.8 oder höher
- **Betriebssystem**: Windows, macOS, Linux
- **RAM**: Mindestens 4GB (8GB empfohlen für KI-Modelle)
- **Festplatte**: 2GB freier Speicherplatz
- **Tesseract OCR**: Für Bildtextextraktion

##  Anwendung starten

### Schnellstart (Empfohlen)
```bash
python run_app.py
```

### Manueller Start

#### Backend starten:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend starten (in einem neuen Terminal):
```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```

##  Zugriff auf die Anwendung

Nach dem Start sind folgende URLs verfügbar:

- **Frontend (Benutzeroberfläche)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API-Dokumentation**: http://localhost:8000/docs
- **Alternative API-Docs**: http://localhost:8000/redoc

##  Verwendung

### 1. Benutzerregistrierung
1. Öffnen Sie http://localhost:8501
2. Wechseln Sie zum "Register"-Tab
3. Erstellen Sie ein neues Benutzerkonto

### 2. Dokumente hochladen
1. Melden Sie sich an
2. Gehen Sie zu "Documents" → "Upload"
3. Wählen Sie eine Datei aus (PDF, DOCX, TXT, JPG, PNG)
4. Wählen Sie optional eine Kategorie
5. Klicken Sie auf "Upload Document"

### 3. Dokumente analysieren
- **Automatische Analyse**: Wird beim Upload durchgeführt
- **Fragen stellen**: Nutzen Sie das Q&A-Feature für spezifische Fragen
- **Suchen**: Durchsuchen Sie alle Dokumente semantisch
- **Kategorien**: Lassen Sie Dokumente automatisch klassifizieren

### 4. Dashboard nutzen
- Übersicht über alle Ihre Dokumente
- Statistiken und Metriken
- Kategorie-Verteilungen
- Kürzlich verarbeitete Dokumente

### Authentifizierung
- `POST /api/auth/register` - Benutzerregistrierung
- `POST /api/auth/login` - Benutzeranmeldung
- `GET /api/auth/me` - Benutzerprofil abrufen

### Dokumente
- `POST /api/documents/upload` - Dokument hochladen
- `GET /api/documents/` - Alle Dokumente abrufen
- `GET /api/documents/{id}` - Einzelnes Dokument abrufen
- `POST /api/documents/{id}/query` - Dokument befragen
- `POST /api/documents/search` - Semantische Suche
- `DELETE /api/documents/{id}` - Dokument löschen

### Analytics
- `GET /api/analytics/dashboard` - Dashboard-Statistiken

##  Entwicklung

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
├── requirements.txt           # Python-Abhängigkeiten
├── .env                      # Umgebungsvariablen
├── run_app.py               # Startskript
└── README.md                # Diese Datei
```

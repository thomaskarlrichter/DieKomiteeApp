# Wortmeldungs-App

Eine vollständige Flask-Webanwendung für Wortmeldungen und Rückmeldungen.

## Features

- **Benutzer-Authentifizierung** – Registrierung, Login/Logout, Passwort-Hashing (PBKDF2 via Werkzeug)
- **Persönliche Profilseiten** – Jeder User hat eine eigene Seite unter `/user/<username>`
- **Wortmeldungen** – Erstellen, Anzeigen, Löschen eigener Beiträge
- **Rückmeldungen** – Kommentare zu Wortmeldungen von allen eingeloggten Usern
- **CSRF-Schutz** – Alle Formulare via Flask-WTF abgesichert
- **Responsives Design** – Bootstrap 5 + Bootstrap Icons, deutsche Oberfläche
- **Paginierung** – Feed und Profilseiten (10 Einträge/Seite)

## Tech Stack

| Komponente   | Technologie                   |
|--------------|-------------------------------|
| Backend      | Python Flask 3.0              |
| ORM / DB     | SQLAlchemy + SQLite           |
| Auth         | Flask-Login                   |
| CSRF-Schutz  | Flask-WTF                     |
| Frontend     | Bootstrap 5 + Bootstrap Icons |

## Installation & Start

```bash
# 1. In Projektverzeichnis wechseln
cd wortmeldung-app

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. App starten
python app.py
```

Die App ist erreichbar unter: **http://localhost:5000**

Die SQLite-Datenbank (`instance/wortmeldung.db`) wird beim ersten Start automatisch erstellt.

## Projektstruktur

```
wortmeldung-app/
├── app.py                   Flask-Applikation & alle Routen
├── models.py                SQLAlchemy-Modelle
├── requirements.txt         Python-Abhängigkeiten
├── README.md                Diese Datei
├── templates/
│   ├── base.html            Basis-Layout (Navbar, Flash-Messages)
│   ├── index.html           Startseite / Feed
│   ├── login.html           Anmelde-Formular
│   ├── register.html        Registrierungs-Formular
│   ├── profile.html         Profilseite
│   ├── wortmeldung.html     Detail-Ansicht + Rückmeldungen
│   ├── wortmeldung_neu.html Neue Wortmeldung erstellen
│   └── error.html           Fehlerseite (403, 404)
└── static/
    └── style.css            Zusätzliche CSS-Styles
```

## Routen

| Route                                      | Methode   | Beschreibung                           |
|--------------------------------------------|-----------|----------------------------------------|
| `/`                                        | GET       | Feed aller Wortmeldungen               |
| `/register`                                | GET, POST | Registrierung                          |
| `/login`                                   | GET, POST | Anmeldung                              |
| `/logout`                                  | GET       | Abmeldung                              |
| `/user/<username>`                         | GET       | Profilseite                            |
| `/wortmeldung/neu`                         | GET, POST | Neue Wortmeldung (login required)      |
| `/wortmeldung/<id>`                        | GET       | Detail + Rückmeldungen                 |
| `/wortmeldung/<id>/loeschen`               | POST      | Wortmeldung löschen (Eigentümer)       |
| `/wortmeldung/<id>/rueckmeldung`           | POST      | Rückmeldung erstellen (login required) |
| `/rueckmeldung/<id>/loeschen`              | POST      | Rückmeldung löschen (Eigentümer)       |

## Sicherheit

- Passwörter gehasht mit `werkzeug.security.generate_password_hash` (PBKDF2)
- CSRF-Token auf allen POST-Formularen
- `@login_required` schützt alle schreibenden Routen
- HTTP 403 bei Zugriffsversuchen auf fremde Inhalte
- Secret Key via Umgebungsvariable konfigurierbar: `SECRET_KEY=...`

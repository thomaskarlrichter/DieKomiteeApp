# Die Komitee-App - TODO & Feature-Backlog

Dieses Dokument enthält geplante Erweiterungen und Ideen für die Weiterentwicklung der Komitee-App.

## 1. Verbesserte Treffen- & Protokollverwaltung (Ausbau der Kernfunktion)
- [ ] **Live-Protokoll-Modus (Für die Leitung)**
  - Ansicht für laufende Treffen entwickeln.
  - Schneller Status-Wechsel (z.B. "erledigt", "zurückgestellt") für Wortmeldungen.
  - Feld für Live-Notizen hinzufügen.
- [ ] **Agenda-Generierung & PDF-Export**
  - Automatische PDF-Agenda vor dem Treffen generieren (sortiert nach Kategorien).
  - PDF-Protokoll nach dem Treffen exportieren (mittels `fpdf2`).
- [ ] **Kalender-Integration (.ics)**
  - `.ics`-Export für Treffen implementieren (für Apple Calendar, Google Calendar, Outlook).
- [ ] **Teilnehmer-Management (RSVP)**
  - Funktionen für "Ich nehme teil" / "Ich fehle entschuldigt" bei Treffen hinzufügen.

## 2. Persönliche Begleitung & Genesung (12-Schritte-Fokus)
- [ ] **Sponsoring / Mentoren-System**
  - Datenmodell für Sponsor-Mentee-Verknüpfungen erstellen.
  - Lesezugriff für Sponsoren auf Auflagen und Rückfälle (mit Opt-In des Mentees).
- [ ] **Meilensteine & Clean-Zeit-Zähler**
  - Logik zur Berechnung der "Tage seit Beginn der Auflage" bzw. "Tage seit dem letzten Rückfall" implementieren.
  - Visuelle Auszeichnungen (Chips/Badges) für Meilensteine (z.B. 30 Tage, 90 Tage, 1 Jahr) im Profil anzeigen.
- [ ] **Tägliches Check-in / Tagebuch**
  - Leichtgewichtiges Modell für tägliche Einträge (Stimmung, Dankbarkeit) ergänzen.

## 3. Usability & Benutzererfahrung
- [ ] **E-Mail-Benachrichtigungen**
  - E-Mail-Versand integrieren.
  - Benachrichtigung bei neuen Rückmeldungen zu eigenen Wortmeldungen.
  - Erinnerungs-E-Mails 24h vor einem anstehenden Treffen.
- [ ] **Erweiterte Such- und Filterfunktionen**
  - Such- und Filter-UI auf Übersichtsseiten (Treffen, Auflagen, Wortmeldungen) hinzufügen (z.B. Filtern nach Datum, Status oder Kategorie).
- [ ] **Archivierungs-System**
  - "Archiviert"-Status für alte Treffen und Wortmeldungen (z.B. älter als 6 Monate) hinzufügen, um die UI sauber zu halten.
  - Archiv-Ansicht erstellen.

## 4. Administration & Datenschutz
- [ ] **Granulare Sichtbarkeit / Datenschutz**
  - Sichtbarkeits-Level für Wortmeldungen einführen (z.B. "Alle", "Nur Leitung", "Nur Treffen-Teilnehmer").
- [ ] **Statistiken & Dashboard**
  - Dashboard für individuelle Nutzer-Statistiken erstellen.
  - Anonymisiertes Dashboard für die Komiteeleitung erstellen (z.B. Treffen-Besuchsstatistiken).
- [ ] **Einfache Textformatierung (Rich Text)**
  - WYSIWYG-Editor (wie Quill oder CKEditor) für mehrzeilige Textfelder (Wortmeldungen, Auflagen, Rückfälle) integrieren.

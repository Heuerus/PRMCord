# Anmerkungen

## Projektaufbau 
- Grundsätzliche Parts die normalerweise in einem Projekt vorkommen
    - .gitignore -> Dateien die nicht gepusht werden sollen (z.B. .idea Ordner, config Dateien, cache Dateien -> beim Erstellen eines Repos über z.B. Github kann eine Vorlage für Python ausgewählt werden, die bereits cache Dateien etc. ausschließt)
    - requirements.txt -> alle benötigten Libraries, um diese schnell installieren zu können (pip install -r requirements.txt) -> gerade auch sinnvoll, um mit virtuelle Umgebungen (venv) zu arbeiten
    - README.md -> Beschreibung des Projekts: grobe Struktur, was das Projekt macht, wie es aufgebaut ist und vor allem auch wie man es zum laufen bringt
    - config.json oder .env -> Konfigurationsdateien, um z.B. API-Keys oder andere sensible Informationen zu speichern (sind auch einfacher anzupassen als direkt im Code -> "erlaubte Channel" z.B. könnte man dort auch hinterlegen)
- 

- Extras bei großen Projekten:
    - Tests -> um sicherzustellen, dass Änderungen keine Fehler verursachen
    - Dokumentation -> um anderen Entwicklern zu zeigen, wie das Projekt funktioniert
    - Logging -> um Fehler zu finden und zu beheben
    - CI/CD -> um automatisiert zu testen und zu deployen

## Notizen
- Ich persönlich bin Fan eines ORM (Object Relational Mapper) Ansatzes, um mit Datenbanken zu arbeiten. Für Python gibt es hierfür z.B. SQLAlchemy. -> ORM ist eine Technik, die es ermöglicht, Datenbanken über Objekte zu manipulieren, anstatt SQL-Queries zu schreiben.
- Sprunghafter Wechsel zwischen deutscher und englischer Sprache 
- 
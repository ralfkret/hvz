# hvz
Repo für das Haushalts-Verwaltungs-System - kurz HVS oder auch Haferzähler.

## Planung
Planung findet im [GitHub Projekt](https://github.com/ralfkret/hvz/projects/1) statt.

## Übersicht über die Komponenten
```
+---------------+
|               |
| Mobile Client +-------+
| (Kotlin)      |       |
|               |       |      +---------------+          +---------------+
+---------------+       |      |               |          |               |
                        +------+ API           +----------+ Data          |
+---------------+       |      | (Django)      |          | (Postgresql)  |
|               |       |      |               |          |               |
| Web Client    +-------+      +---------------+          +---------------+
| (React)       |
|               |
+---------------+
```


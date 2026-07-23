RESONANZ – Pretest-Auswertung
Skriptbasierte Auswertung des Pretests zur Mental-Health-App RESONANZ.
Hochschule Furtwangen (HFU), Standort Rottweil
Studiengang Angewandte Gesundheitsförderung · Sommersemester 2026
Andreas Braxmeier
---
Zweck
Dieses Repositorium enthält den vollständigen Auswertungsweg des Pretests: vom
unveränderten Rohdatenexport bis zum fertigen Ergebnisdokument mit Kennwerten,
Tabellen und Abbildungen.
Ziel ist die Reproduzierbarkeit. Alle im Bericht genannten Zahlen lassen
sich durch einmaliges Ausführen des Skripts identisch nachvollziehen. Es wurden
keine Werte manuell eingetragen, nachgerechnet oder nachträglich korrigiert.
---
Inhalt
Datei	Beschreibung
`auswertung_resonanz.py`	Auswertungsskript
`Pretest_Export_soscisurvey.xlsx`	Unveränderter Rohdatenexport aus SoSci Survey
`README.md`	Diese Anleitung
Beim Ausführen wird zusätzlich die Datei
`RESONANZ_Auswertung_Ergebnis.docx` erzeugt. Sie enthält alle Tabellen und
beide Abbildungen. Die Abbildungen werden direkt in das Word-Dokument
eingebettet und nicht als separate Bilddateien gespeichert.
---
Ausführen
Voraussetzungen
Python 3.9 oder neuer sowie drei Bibliotheken:
```
pip install openpyxl matplotlib python-docx
```
Aufruf
```
python auswertung_resonanz.py
```
Skript und Excel-Datei müssen im selben Ordner liegen. Das Skript sucht die
Excel-Datei relativ zum Arbeitsverzeichnis.
Ergebnis
In der Konsole werden die Fallzahlen ausgegeben. Im selben Ordner entsteht das
Word-Ergebnisdokument mit folgenden Abschnitten:
Fallzahlen
Stichprobenbeschreibung
Vorerfahrung: genutzte Apps und Zufriedenheit
Einzelitems
Kurzskalen
Antwortverteilungen
Abbildungen
Offene Antworten
Ein bestehendes Ergebnisdokument wird dabei überschrieben.
---
Methodische Entscheidungen
Die folgenden Punkte sind bewusst so umgesetzt und für das Verständnis der
Ergebnisse relevant.
Deskriptive Auswertung.
Der Pretest dient der Konzept- und Instrumentenprüfung, nicht der
Hypothesentestung. Es werden daher ausschließlich Häufigkeiten, Mittelwerte
und Streuungen berichtet; auf Signifikanztests wird bewusst verzichtet.
Keine Imputation.
Leere Zellen gelten als fehlender Wert und werden nicht ersetzt. Die Fallzahl
unterscheidet sich deshalb zwischen den Fragebogenblöcken, weil Teilnehmende
an unterschiedlichen Stellen abgebrochen haben. Die jeweils gültige Fallzahl
wird bei jedem Kennwert mit ausgewiesen.
Standardabweichung.
Verwendet wird `statistics.pstdev` (Populationsvarianz, Teiler n). Die
vorliegenden Fälle werden als vollständige beobachtete Menge behandelt und
nicht als Zufallsstichprobe aus einer definierten Grundgesamtheit, da die
Rekrutierung als Gelegenheitsstichprobe erfolgte.
Zweistufige Skalenbildung.
Kurzskalen werden in zwei Schritten gebildet: zunächst je Person der
Mittelwert über die zugehörigen Items, anschließend der Mittelwert über alle
Personen. Eine Person geht nur ein, wenn sie alle Items der Skala beantwortet
hat (listenweiser Ausschluss). Das verhindert, dass Personen mit wenigen
Antworten die Skala verzerren.
Negativ gepoltes Item.
Item `A303` (Datenschutz-Bedenken) ist negativ gepolt – ein hoher Wert bedeutet
mehr Sorge. Es geht deshalb in keine der positiv gepolten Kurzskalen ein und
wird ausschließlich einzeln berichtet. Eine Umkodierung findet nicht statt.
Aufbau des SoSci-Exports.
Zeile 1 enthält die Variablenkürzel (`A101`, `A201`, …), Zeile 2 die
Klartextbezeichnungen, ab Zeile 3 folgen die Daten – eine Zeile je
Fragebogenaufruf. Das Skript liest ab Zeile 3 und ist damit direkt an das
Exportformat gekoppelt; die Datei wurde nicht nachbearbeitet.
---
Kurzskalen
Skala	Items
S1 Attraktivität und Akzeptanz	A201, A202, A204, A207
S2 Nutzungsintention	A207, A208
S3 Verständlichkeit	A301, A302
S4 Gamification-Akzeptanz	A204, A205, A206
Antwortformat durchgehend fünfstufig (1 = trifft überhaupt nicht zu bis
5 = trifft voll und ganz zu). Die Skalenmitte (3) ist in beiden Abbildungen
als gestrichelte Linie eingezeichnet.
---
Datenschutz
Der Datensatz enthält ausschließlich anonyme Angaben. Die Teilnahme erfolgte
freiwillig nach Aufklärung über Zweck und Verwendung der Daten. Direkt oder
indirekt identifizierende Merkmale wurden nicht erhoben bzw. vor der
Veröffentlichung entfernt.
---
Hinweis zur Verwendung
Der Code entstand im Rahmen einer Studienleistung und ist auf genau diesen
Datensatz zugeschnitten. Eine Übertragung auf andere Erhebungen erfordert
Anpassungen an Variablenkürzeln, Skalenzuordnung und Kategorienlabels.

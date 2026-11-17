# Colonia CyberAnts (Grupo 2) — Proyecto ANTDRON (KGD)

Aplicación táctica desarrollada con **Extreme Programming (XP)** en Python 3.12 + Flask + SQLite + pytest + Docker.
Archivo de coordenadas: `data/Grupo02.csv` (60 filas generadas con los 10 dígitos de las 6 cédulas).
Hormiga del Grupo 2: `HSoldado` (evoluciona y vive con `Carnívoro`).
Lenguaje del Autómata: `L = { a+, ab*, ab*t+, abcdt+ }`.

## Integrantes y Cédulas
| # | Cédula | Integrante | Último Dígito | Coordenada | Expresión | Rol XP | Rol Hormiguero |
| :- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| 1 | `0402132500` | Chuga Juan | `0` | `Coord-00` | `a+` | Programador (Pareja 1) | Hormiga Soldado |
| 2 | `1755580402` | Camino Emilio | `2` | `Coord-02` | `ab*` | Coach XP + Tracker | Hormiga Exploradora |
| 3 | `0503855330` | Casa Fernando | `0` | `Coord-00` | `a+` | Programador (Pareja 1) | Hormiga Obrera |
| 4 | `1726339151` | Carcelén Josue | `1` | `Coord-01` | `a+` | Programador (Pareja 2) | Hormiga Centinela |
| 5 | `1729044121` | Carrera Fernando | `1` | `Coord-01` | `a+` | Programador (Pareja 2) | Hormiga Nodriza |
| 6 | `1005444912` | Cartagena Franciss | `2` | `Coord-02` | `ab*` | Cliente / Product Owner | Hormiga Reina |

## Ejecución Rápida
```bash
# 1. Ejecutar pruebas unitarias (TDD)
pytest -v

# 2. Levantar aplicación web en local (http://localhost:5000)
python -m src.app

# 3. Ejecutar salida exacta en consola
python -m src.console

# 4. Levantar con Docker
docker compose up --build
```

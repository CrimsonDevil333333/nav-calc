# NavCalc Pro 🦞⚓

A high-performance Maritime Engineering and Navigation CLI tool. Built for Marine Engineers, Deck Officers, and Logistics Managers who need rapid, accurate, and professional-grade maritime calculations.

## For Whom? 🚢
- **Marine Engineers**: Track fuel efficiency (SFOC) and propulsion performance (Slip).
- **Deck Officers**: Rapid voyage planning, ETA estimation, and Great Circle distance checks.
- **Logistics Managers**: Estimate bunkering requirements for voyages using the Cube Law.

## Advanced Features 🚀

- **Interactive Console**: Run `python3 main.py` without arguments to enter a menu-driven, interactive session.
- **Voyage Suite**: Calculate Speed, Time, Distance, and multi-leg ETAs.
- **Engineering Module**:
  - **Propeller Slip**: Compare engine speed vs. actual speed over ground.
  - **SFOC Engine**: Calculate Specific Fuel Oil Consumption ($g/kWh$).
- **Fuel Cube Law**: Advanced estimation using ship-specific consumption curves ($F \propto S^3$).
- **Rich Visualization**: Fully formatted tables, panels, and progress indicators for all calculations.

## Installation 📦

```bash
pip install rich
```

## Quick Start 🛠️

### 1. Interactive Mode (Menu Driven)
Simply run:
```bash
python3 main.py
```

### 2. SFOC Calculation (Engineering)
*Calculate efficiency for an engine consuming 1200kg/hr at 8000kW:*
```bash
# Available via Interactive Menu -> Engineering -> SFOC
```

### 3. Great Circle Distance (Navigation)
```bash
python3 main.py dist 18.97 72.82 25.27 55.23
```

---
*Maintained by Satyaa & Clawdy*

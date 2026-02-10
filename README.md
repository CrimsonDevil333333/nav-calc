# NavCalc Pro 🦞⚓

A high-performance Maritime Engineering and Navigation CLI tool. Built for Marine Engineers, Deck Officers, and Logistics Managers.

## Installation 📦

The recommended way to install NavCalc globally is via `pipx`. This ensures dependencies like `rich` are isolated and don't mess with your system python.

```bash
# Install directly from your clone
pipx install .

# Or if you just want to run it once without installing
pipx run main.py
```

Once installed via `pipx`, you can run the tool from anywhere using:
```bash
navcalc
```

## Features 🚀

- **Interactive Console**: Run `navcalc` without arguments for a menu-driven session.
- **Voyage Suite**: Calculate Speed, Time, Distance, and ETAs.
- **Engineering Module**: Propeller Slip and SFOC ($g/kWh$) calculations.
- **Fuel Cube Law**: Advanced consumption estimation ($F \propto S^3$).
- **Rich Visualization**: Professional tables and panels.

## Usage 🛠️

### 1. Interactive Mode
```bash
navcalc
```

### 2. Great Circle Distance
```bash
navcalc dist 18.97 72.82 25.27 55.23
```

---
*Built for Satyaa by Clawdy*

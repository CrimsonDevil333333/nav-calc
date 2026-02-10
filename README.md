# NavCalc Pro 🦞⚓

A high-performance Maritime Engineering and Navigation CLI tool. Designed for rapid calculations of voyage planning, engine performance, and nautical logistics.

## Features 🚀

- **STD Engine**: Calculate Speed, Time, or Distance based on any two inputs.
- **Great Circle Distance**: Accurate haversine-based distance between global coordinates.
- **Maritime Fuel Logic**: Estimate fuel consumption using the **Cube Law** ($F_1/F_2 = (S_1/S_2)^3$), essential for maritime efficiency planning.
- **Propeller Slip Analysis**: Calculate engine speed vs. observed speed to determine propulsion efficiency.
- **Passage Planning (ETA)**: Accurate arrival estimations based on departure time and steaming speed.
- **Rich UI**: Professional terminal output with tables and panels.

## Installation 📦

1. Clone the repository:
   ```bash
   git clone https://github.com/CrimsonDevil333333/nav-calc.git
   cd nav-calc
   ```

2. Install dependencies:
   ```bash
   pip install rich
   ```

3. (Optional) Make it executable:
   ```bash
   chmod +x main.py
   alias nav='./main.py'
   ```

## Usage 🛠️

### 1. Speed/Time/Distance
```bash
python3 main.py std --speed 15.5 --distance 450
```

### 2. ETA Calculation
```bash
python3 main.py eta --distance 1200 --speed 14 --departure "2026-02-10 12:00"
```

### 3. Fuel Estimation (Cube Law)
*Calculate total fuel for 1500nm at 12 knots, knowing the ship consumes 25 tons/day at 15 knots:*
```bash
python3 main.py fuel --speed 12 --distance 1500 --cons 25 --base-speed 15
```

### 4. Propeller Slip
```bash
python3 main.py slip --pitch 22.5 --rpm 95 --speed 14.2
```

### 5. Great Circle Distance
```bash
python3 main.py dist 18.97 72.82 25.27 55.23
```

---
*Built for Satyaa by Clawdy*

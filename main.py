#!/usr/bin/env python3
import sys
import math
import argparse
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.live import Live
from rich.layout import Layout

console = Console()

class NavCalc:
    @staticmethod
    def calculate_std(speed=None, time=None, distance=None):
        if speed and time:
            return {"type": "Distance", "value": f"{speed * time:.2f} nm"}
        if distance and time:
            return {"type": "Speed", "value": f"{distance / time:.2f} knots"}
        if distance and speed:
            t = distance / speed
            return {"type": "Time", "value": f"{t:.2f} hours", "duration": str(timedelta(hours=t)).split('.')[0]}
        return None

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 3440.065  # nm
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

    @staticmethod
    def cube_law_fuel(speed, distance, base_cons, base_speed):
        daily_cons = base_cons * (speed / base_speed)**3
        total_fuel = daily_cons * ((distance / speed) / 24)
        return total_fuel, daily_cons

    @staticmethod
    def propeller_slip(pitch, rpm, actual_speed):
        engine_speed = (pitch * rpm * 60) / 6080
        slip = ((engine_speed - actual_speed) / engine_speed) * 100 if engine_speed > 0 else 0
        return slip, engine_speed

    @staticmethod
    def calculate_sfoc(fuel_per_hour_kg, power_kw):
        """Specific Fuel Oil Consumption (g/kWh)"""
        return (fuel_per_hour_kg * 1000) / power_kw if power_kw > 0 else 0

def interactive_mode():
    nav = NavCalc()
    console.print(Panel.fit("[bold yellow]NavCalc Pro: Interactive Maritime Console[/bold yellow]", border_style="cyan"))
    
    while True:
        console.print("\n[bold cyan]1.[/bold cyan] Voyage (STD/ETA)  [bold cyan]2.[/bold cyan] Fuel/Efficiency  [bold cyan]3.[/bold cyan] Engineering (Slip/SFOC)  [bold cyan]q.[/bold cyan] Quit")
        choice = Prompt.ask("Select Module", choices=["1", "2", "3", "q"])

        if choice == "1":
            dist = FloatPrompt.ask("Distance (nm)")
            speed = FloatPrompt.ask("Speed (kts)")
            hours = dist / speed
            arrival = datetime.now() + timedelta(hours=hours)
            
            table = Table(title="Passage Report")
            table.add_row("Duration", f"{hours:.2f} hrs")
            table.add_row("ETA", arrival.strftime("%Y-%m-%d %H:%M"))
            console.print(table)

        elif choice == "2":
            dist = FloatPrompt.ask("Voyage Distance (nm)")
            speed = FloatPrompt.ask("Transit Speed (kts)")
            base_c = FloatPrompt.ask("Base Consumption (tons/day)")
            base_s = FloatPrompt.ask("at Base Speed (kts)", default=15.0)
            
            total, daily = nav.cube_law_fuel(speed, dist, base_c, base_s)
            console.print(Panel(f"Total Fuel: [bold green]{total:.2f} tons[/bold green]\nDaily Rate: {daily:.2f} t/day"))

        elif choice == "3":
            sub = Prompt.ask("Sub-module", choices=["slip", "sfoc"])
            if sub == "slip":
                p, r, s = FloatPrompt.ask("Pitch (ft)"), FloatPrompt.ask("RPM"), FloatPrompt.ask("Actual Speed (kts)")
                slip, es = nav.propeller_slip(p, r, s)
                console.print(f"Engine Speed: {es:.2f} kts | Slip: [bold]{slip:.2f}%[/bold]")
            else:
                f, p = FloatPrompt.ask("Fuel Flow (kg/hr)"), FloatPrompt.ask("Engine Power (kW)")
                console.print(f"SFOC: [bold green]{nav.calculate_sfoc(f, p):.2f} g/kWh[/bold green]")

        elif choice == "q": break

def main():
    if len(sys.argv) == 1:
        interactive_mode()
        return

    parser = argparse.ArgumentParser(description="NavCalc Pro")
    subparsers = parser.add_subparsers(dest="command")
    
    # Modules (minimal flags for CLI use)
    std_p = subparsers.add_parser("std"); std_p.add_argument("-s", "--speed", type=float); std_p.add_argument("-t", "--time", type=float); std_p.add_argument("-d", "--distance", type=float)
    dist_p = subparsers.add_parser("dist"); dist_p.add_argument("lat1", type=float); dist_p.add_argument("lon1", type=float); dist_p.add_argument("lat2", type=float); dist_p.add_argument("lon2", type=float)
    fuel_p = subparsers.add_parser("fuel"); fuel_p.add_argument("-s", "--speed", type=float, required=True); fuel_p.add_argument("-d", "--distance", type=float, required=True); fuel_p.add_argument("-c", "--cons", type=float, required=True)
    
    args = parser.parse_args()
    nav = NavCalc()

    if args.command == "std":
        res = nav.calculate_std(args.speed, args.time, args.distance)
        console.print(Panel(f"{res['type']}: {res['value']}", expand=False))
    elif args.command == "dist":
        console.print(f"Distance: {nav.haversine(args.lat1, args.lon1, args.lat2, args.lon2):.2f} nm")

if __name__ == "__main__":
    main()

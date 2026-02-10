#!/usr/bin/env python3
import sys
import math
import argparse
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class NavCalc:
    @staticmethod
    def calculate_std(speed=None, time=None, distance=None):
        if speed and time:
            dist = speed * time
            return {"type": "Distance", "value": f"{dist:.2f} nm"}
        if distance and time:
            spd = distance / time
            return {"type": "Speed", "value": f"{spd:.2f} knots"}
        if distance and speed:
            t = distance / speed
            return {"type": "Time", "value": f"{t:.2f} hours", "duration": str(timedelta(hours=t)).split('.')[0]}
        return None

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 3440.065  # Earth radius in nautical miles
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    @staticmethod
    def calculate_fuel(speed, distance, base_consumption, base_speed=15):
        """
        Estimates fuel using the Cube Law: (S1/S2)^3 = F1/F2
        base_consumption: tons/day at base_speed
        """
        daily_cons = base_consumption * (speed / base_speed)**3
        total_time_days = (distance / speed) / 24
        total_fuel = daily_cons * total_time_days
        return total_fuel, daily_cons

    @staticmethod
    def calculate_slip(pitch, rpm, actual_speed):
        """
        Propeller Slip calculation. 
        pitch in feet, actual_speed in knots.
        Engine Speed (knots) = (Pitch * RPM * 60) / 6080
        """
        engine_speed = (pitch * rpm * 60) / 6080
        if engine_speed == 0: return 0
        slip = ((engine_speed - actual_speed) / engine_speed) * 100
        return slip, engine_speed

def main():
    parser = argparse.ArgumentParser(description="NavCalc Pro: Maritime Engineering & Navigation CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available modules")

    # STD
    std_p = subparsers.add_parser("std", help="Speed/Time/Distance Calculations")
    std_p.add_argument("-s", "--speed", type=float, help="Speed in knots")
    std_p.add_argument("-t", "--time", type=float, help="Time in hours")
    std_p.add_argument("-d", "--distance", type=float, help="Distance in nautical miles")

    # Dist
    dist_p = subparsers.add_parser("dist", help="Great Circle Distance between coordinates")
    dist_p.add_argument("lat1", type=float, help="Latitude Start")
    dist_p.add_argument("lon1", type=float, help="Longitude Start")
    dist_p.add_argument("lat2", type=float, help="Latitude End")
    dist_p.add_argument("lon2", type=float, help="Longitude End")

    # Fuel
    fuel_p = subparsers.add_parser("fuel", help="Maritime Fuel Consumption (Cube Law)")
    fuel_p.add_argument("-s", "--speed", type=float, required=True, help="Intended speed in knots")
    fuel_p.add_argument("-d", "--distance", type=float, required=True, help="Total distance in nm")
    fuel_p.add_argument("-c", "--cons", type=float, required=True, help="Base consumption (tons/day)")
    fuel_p.add_argument("-b", "--base-speed", type=float, default=15, help="Speed for base consumption (default: 15kts)")

    # Slip
    slip_p = subparsers.add_parser("slip", help="Propeller Slip Calculation")
    slip_p.add_argument("-p", "--pitch", type=float, required=True, help="Propeller Pitch (ft)")
    slip_p.add_argument("-r", "--rpm", type=float, required=True, help="Engine RPM")
    slip_p.add_argument("-s", "--speed", type=float, required=True, help="Actual speed over ground (knots)")

    # ETA
    eta_p = subparsers.add_parser("eta", help="Calculate Estimated Time of Arrival")
    eta_p.add_argument("-d", "--distance", type=float, required=True)
    eta_p.add_argument("-s", "--speed", type=float, required=True)
    eta_p.add_argument("-dep", "--departure", type=str, help="Departure (YYYY-MM-DD HH:MM), defaults to now")

    args = parser.parse_args()
    nav = NavCalc()

    if args.command == "std":
        res = nav.calculate_std(args.speed, args.time, args.distance)
        if res:
            console.print(Panel(f"[bold green]{res['type']}:[/bold green] {res['value']}" + (f" ({res['duration']})" if 'duration' in res else ""), title="STD Result", expand=False))
        else:
            console.print("[red]Error:[/red] Provide two values.")

    elif args.command == "dist":
        d = nav.haversine(args.lat1, args.lon1, args.lat2, args.lon2)
        console.print(Panel(f"[bold cyan]Great Circle Distance:[/bold cyan] {d:.2f} nm", title="Navigation", expand=False))

    elif args.command == "fuel":
        total, daily = nav.calculate_fuel(args.speed, args.distance, args.cons, args.base_speed)
        table = Table(title="Fuel Estimation")
        table.add_column("Metric", style="magenta")
        table.add_column("Value", style="white")
        table.add_row("Total Fuel Required", f"{total:.2f} tons")
        table.add_row("Daily Consumption", f"{daily:.2f} tons/day")
        table.add_row("Voyage Duration", f"{(args.distance/args.speed)/24:.2f} days")
        console.print(table)

    elif args.command == "slip":
        slip, e_speed = nav.calculate_slip(args.pitch, args.rpm, args.speed)
        table = Table(title="Propeller Slip Analysis")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Engine Speed", f"{e_speed:.2f} knots")
        table.add_row("Observed Speed", f"{args.speed:.2f} knots")
        table.add_row("Calculated Slip", f"{slip:.2f}%")
        console.print(table)

    elif args.command == "eta":
        dep = datetime.now()
        if args.departure:
            try: dep = datetime.strptime(args.departure, "%Y-%m-%d %H:%M")
            except: console.print("[red]Format error.[/red] Use YYYY-MM-DD HH:MM"); return
        
        hours = args.distance / args.speed
        arrival = dep + timedelta(hours=hours)
        
        table = Table(title="Passage Planning (ETA)")
        table.add_row("Departure", dep.strftime("%Y-%m-%d %H:%M"))
        table.add_row("Steaming Time", f"{hours:.2f} hours")
        table.add_row("ETA (Arrival)", f"[bold green]{arrival.strftime('%Y-%m-%d %H:%M')}[/bold green]")
        console.print(table)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

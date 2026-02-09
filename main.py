import sys
import math
import argparse
from datetime import datetime, timedelta

def calculate_std(speed=None, time=None, distance=None):
    if speed and time:
        return f"Distance: {speed * time:.2f} nm"
    if distance and time:
        return f"Speed: {distance / time:.2f} knots"
    if distance and speed:
        return f"Time: {distance / speed:.2f} hours ({timedelta(hours=distance/speed)})"
    return "Error: Provide two values to calculate the third."

def calculate_fuel(consumption_rate, time):
    return f"Total Fuel: {consumption_rate * time:.2f} units"

def haversine(lat1, lon1, lat2, lon2):
    R = 3440.065 # Earth radius in nautical miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def main():
    parser = argparse.ArgumentParser(description="NavCalc: Nautical Engineering CLI")
    subparsers = parser.add_subparsers(dest="command")

    # STD Parser
    std_parser = subparsers.add_parser("std", help="Speed/Time/Distance")
    std_parser.add_argument("-s", "--speed", type=float, help="Speed in knots")
    std_parser.add_argument("-t", "--time", type=float, help="Time in hours")
    std_parser.add_argument("-d", "--distance", type=float, help="Distance in nautical miles")

    # Dist Parser
    dist_parser = subparsers.add_parser("dist", help="Great Circle Distance between coordinates")
    dist_parser.add_argument("lat1", type=float)
    dist_parser.add_argument("lon1", type=float)
    dist_parser.add_argument("lat2", type=float)
    dist_parser.add_argument("lon2", type=float)

    args = parser.parse_args()

    if args.command == "std":
        print(calculate_std(args.speed, args.time, args.distance))
    elif args.command == "dist":
        d = haversine(args.lat1, args.lon1, args.lat2, args.lon2)
        print(f"Great Circle Distance: {d:.2f} nm")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

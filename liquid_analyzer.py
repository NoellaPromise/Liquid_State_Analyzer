#!/usr/bin/env python3
"""
Liquid State Analyzer - AUTO-WEB VERSION
Grade 8 Coding Club Project - NLS
Automatically opens web interface and updates it with results
"""

import json
import webbrowser
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket


class LiquidAnalyzer:
    def __init__(self):
        print("🧪 Starting Liquid State Analyzer...")
        self.liquids_data = self.load_liquid_data()

    def load_liquid_data(self):
        try:
            with open("liquids_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            print("✅ Loaded liquid data from liquids_data.json")
            return data
        except FileNotFoundError:
            print("📄 Creating liquids_data.json with default data...")
            default_data = self.get_default_liquids()
            self.save_liquid_data(default_data)
            return default_data

    def get_default_liquids(self):
        return {
            "water": {
                "name": "Water (H₂O)",
                "freezing_point": 0.0,
                "boiling_point": 100.0,
            },
            "ethanol": {
                "name": "Ethanol (C₂H₅OH)",
                "freezing_point": -114.1,
                "boiling_point": 78.4,
            },
            "mercury": {
                "name": "Mercury (Hg)",
                "freezing_point": -38.8,
                "boiling_point": 356.7,
            },
            "nitrogen": {
                "name": "Nitrogen (N₂)",
                "freezing_point": -210.0,
                "boiling_point": -195.8,
            },
            "oxygen": {
                "name": "Oxygen (O₂)",
                "freezing_point": -218.8,
                "boiling_point": -183.0,
            },
        }

    def save_liquid_data(self, data):
        with open("liquids_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        print("💾 Saved liquid data to liquids_data.json")

    def calculate_pressure_effect(self, base_boiling_point, pressure):
        pressure_difference = pressure - 1.0
        adjusted_boiling = base_boiling_point + (pressure_difference * 10.0)
        return adjusted_boiling

    def analyze_liquid_state(self, temperature, pressure, liquid_type):
        if liquid_type not in self.liquids_data:
            raise ValueError(f"Unknown liquid: {liquid_type}")
        if pressure <= 0:
            raise ValueError("Pressure must be greater than 0")

        liquid = self.liquids_data[liquid_type]
        freezing_point = liquid["freezing_point"]
        base_boiling_point = liquid["boiling_point"]
        actual_boiling_point = self.calculate_pressure_effect(
            base_boiling_point, pressure
        )

        if temperature <= freezing_point:
            state = "SOLID"
            flask_state = "frozen"
            description = f"FROZEN! Temperature {temperature}°C is at or below freezing point ({freezing_point}°C)"
        elif temperature >= actual_boiling_point:
            state = "GAS"
            flask_state = "boiling"
            description = f"BOILING! Temperature {temperature}°C is at or above boiling point ({actual_boiling_point:.1f}°C)"
        else:
            state = "LIQUID"
            flask_state = "still"
            description = (
                f"LIQUID state! Temperature is between freezing and boiling points"
            )

        return {
            "liquid_name": liquid["name"],
            "temperature": temperature,
            "pressure": pressure,
            "state": state,
            "flask_state": flask_state,
            "description": description,
            "freezing_point": freezing_point,
            "boiling_point_normal": base_boiling_point,
            "boiling_point_actual": round(actual_boiling_point, 1),
        }

    def save_results_for_web(self, results):
        """Save results in a format the web page can read"""
        web_results = {
            "liquid_name": results["liquid_name"],
            "temperature": results["temperature"],
            "pressure": results["pressure"],
            "state": results["state"],
            "flask_state": results["flask_state"],
            "description": results["description"],
            "timestamp": time.time(),
        }
        with open("current_results.json", "w") as file:
            json.dump(web_results, file, indent=2)
        print("🌐 Results updated for web interface")


def start_local_server():
    """Start a simple web server to serve the HTML files"""
    port = 8000
    try:
        # Check if port is available
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(("localhost", port))
            if result == 0:
                print(f"⚠️ Port {port} already in use")
                return None

        handler = SimpleHTTPRequestHandler
        httpd = HTTPServer(("", port), handler)
        print(f"🌐 Web server starting on http://localhost:{port}")

        # Start server in background thread
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        return httpd
    except Exception as e:
        print(f"❌ Could not start web server: {e}")
        return None


def display_results(results):
    """Display results in terminal"""
    print("\n🧪 LIQUID STATE ANALYSIS RESULTS 🧪")
    print("=" * 50)
    print(
        f"🔬 {results['liquid_name']} | 🌡️ {results['temperature']}°C | 📏 {results['pressure']} atm"
    )
    print(f"🏷️ STATE: {results['state']}")
    print(f"📖 {results['description']}")
    print("=" * 50)


def get_user_input(analyzer):
    """Get input from user"""
    print("\n🎯 Let's analyze a liquid state!")
    liquids = analyzer.liquids_data
    print("📋 Available liquids:")
    liquid_list = list(liquids.keys())
    for i, liquid_key in enumerate(liquid_list, 1):
        liquid_info = liquids[liquid_key]
        print(f" {i}. {liquid_info['name']}")

    while True:
        try:
            choice = input(f"\n🔤 Choose a liquid (1-{len(liquid_list)}): ")
            choice_num = int(choice)
            if 1 <= choice_num <= len(liquid_list):
                liquid_type = liquid_list[choice_num - 1]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(liquid_list)}")
        except ValueError:
            print("❌ Please enter a valid number")

    while True:
        try:
            temperature = float(input("🌡️ Enter temperature in Celsius: "))
            break
        except ValueError:
            print("❌ Please enter a valid number")

    while True:
        try:
            pressure_input = input("📏 Enter pressure in atm (press Enter for 1.0): ")
            if pressure_input.strip() == "":
                pressure = 1.0
            else:
                pressure = float(pressure_input)
            if pressure > 0:
                break
            else:
                print("❌ Pressure must be greater than 0")
        except ValueError:
            print("❌ Please enter a valid number")

    return temperature, pressure, liquid_type


def main():
    """Main program - automatically starts web interface"""
    try:
        print("🧪 Welcome to Liquid State Analyzer!")
        print("🌐 Starting web interface automatically...")
        print("=" * 50)

        # Start web server
        server = start_local_server()

        # Open browser after a short delay
        time.sleep(1)
        if server:
            webbrowser.open("http://localhost:8000/index.html")
            print("✅ Web interface opened in your browser!")
        else:
            print("⚠️ Web server couldn't start, running terminal-only mode")

        analyzer = LiquidAnalyzer()

        while True:
            temperature, pressure, liquid_type = get_user_input(analyzer)
            print("\n🔬 Analyzing...")
            results = analyzer.analyze_liquid_state(temperature, pressure, liquid_type)

            # Show results in terminal
            display_results(results)

            # Save results for web interface
            analyzer.save_results_for_web(results)
            print("🔄 Web interface updated! Check your browser.")

            continue_choice = input("\n🔄 Analyze another liquid? (y/n): ").lower()
            if continue_choice != "y":
                print("\n🎉 Thanks for using Liquid State Analyzer!")
                if server:
                    print("🌐 You can keep the web page open to view your results")
                break

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as error:
        print(f"❌ Error: {error}")


if __name__ == "__main__":
    main()

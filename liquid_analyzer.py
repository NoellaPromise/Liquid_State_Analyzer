#!/usr/bin/env python3
"""
Liquid State Analyzer - COACH VERSION (Complete Working Code)
This is the complete working version for the coach to demonstrate
Grade 8 Coding Club Project - NLS
"""

# Import the libraries we need
import json  # For reading and writing JSON files
import os  # For checking if files exist
import webbrowser  # For opening web browser automatically
import time  # For adding delays


class LiquidAnalyzer:
    """This class analyzes liquid states like a smart chemistry calculator"""

    def __init__(self):
        """This runs when we create a new LiquidAnalyzer"""
        print("🧪 Starting Liquid State Analyzer...")
        # Load liquid data from JSON file
        self.liquids_data = self.load_liquid_data()

        # ASCII art for different flask states
        self.flask_art = {
            "still": """
    LIQUID (Still)
         ___
        |   |
        |   |
      __|___|__
     |         |
     |  ~~~~~  |   💧
     |  ~~~~~  |
     |  ~~~~~  |
     |_________|
            """,
            "frozen": """
    SOLID (Frozen) 
         ___
        |   |
        |   |
      __|___|__
     |         |
     |  ❄️ ❄️ ❄️ |   🧊
     |  ❄️ ❄️ ❄️ |
     |  ❄️ ❄️ ❄️ |
     |_________|
            """,
            "boiling": """
    GAS (Boiling)
         ___     💨 💨
        | ° |  💨  💨 💨
        | ° |   💨  💨
      __|°__|__ 💨  💨
     |    °    |
     |  ° ° °  |   🔥
     | ° ° ° ° |
     | ° ° ° ° |
     |_________|
            """,
        }

    def load_liquid_data(self):
        """Load liquid information from JSON file"""
        try:
            # Try to open and read the JSON file
            with open("liquids_data.json", "r") as file:
                data = json.load(file)
                print("✅ Loaded liquid data from liquids_data.json")
                return data
        except FileNotFoundError:
            # If file doesn't exist, create it with default data
            print("📄 Creating liquids_data.json with default data...")
            default_data = self.get_default_liquids()
            self.save_liquid_data(default_data)
            return default_data

    def get_default_liquids(self):
        """Return default liquid data"""
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
        """Save liquid data to JSON file"""
        with open("liquids_data.json", "w") as file:
            json.dump(data, file, indent=2)
        print("💾 Saved liquid data to liquids_data.json")

    def get_available_liquids(self):
        """Get list of available liquids"""
        return self.liquids_data

    def calculate_pressure_effect(self, base_boiling_point, pressure):
        """Calculate how pressure affects boiling point"""
        # Simple formula: each 1 atm change affects boiling by 10°C
        pressure_difference = pressure - 1.0  # Standard pressure is 1 atm
        adjusted_boiling = base_boiling_point + (pressure_difference * 10.0)
        return adjusted_boiling

    def analyze_liquid_state(self, temperature, pressure, liquid_type):
        """Main function that analyzes liquid state"""

        # Check if liquid exists in our data
        if liquid_type not in self.liquids_data:
            raise ValueError(f"Unknown liquid: {liquid_type}")

        # Check if pressure is valid
        if pressure <= 0:
            raise ValueError("Pressure must be greater than 0")

        # Get liquid information
        liquid = self.liquids_data[liquid_type]
        freezing_point = liquid["freezing_point"]
        base_boiling_point = liquid["boiling_point"]

        # Calculate actual boiling point with pressure effect
        actual_boiling_point = self.calculate_pressure_effect(
            base_boiling_point, pressure
        )

        # Determine liquid state
        if temperature <= freezing_point:
            # It's frozen (solid)
            state = "SOLID"
            flask_state = "frozen"
            description = f"FROZEN! Temperature {temperature}°C is at or below freezing point ({freezing_point}°C)"

        elif temperature >= actual_boiling_point:
            # It's boiling (gas)
            state = "GAS"
            flask_state = "boiling"
            description = f"BOILING! Temperature {temperature}°C is at or above boiling point ({actual_boiling_point:.1f}°C)"

        else:
            # It's normal liquid
            state = "LIQUID"
            flask_state = "still"
            description = (
                f"LIQUID state! Temperature is between freezing and boiling points"
            )

        # Return all results
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
            "flask_art": self.flask_art[flask_state],
        }

    def save_analysis_result(self, results):
        """Save analysis results to JSON file"""
        # Add timestamp
        import datetime

        results_with_time = results.copy()
        results_with_time["analysis_time"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Remove flask_art from saved data (it's just for display)
        if "flask_art" in results_with_time:
            del results_with_time["flask_art"]

        # Load existing results
        if os.path.exists("analysis_results.json"):
            with open("analysis_results.json", "r") as file:
                all_results = json.load(file)
        else:
            all_results = []

        # Add new result
        all_results.append(results_with_time)

        # Save back to file
        with open("analysis_results.json", "w") as file:
            json.dump(all_results, file, indent=2)

        print("💾 Results saved to analysis_results.json")

    def create_web_results(self, results):
        """Create a simple HTML file with results for the web interface"""
        html_content = f"""
        <script>
        // Auto-update the web interface with results
        const results = {{
            liquid_name: "{results['liquid_name']}",
            temperature: {results['temperature']},
            pressure: {results['pressure']},
            state: "{results['state']}",
            flask_state: "{results['flask_state']}",
            description: "{results['description']}"
        }};
        
        // Update the webpage if it's open
        if (window.parent && window.parent.displayResults) {{
            window.parent.displayResults(results);
        }}
        </script>
        """

        with open("web_results.html", "w") as file:
            file.write(html_content)


def display_results(results):
    """Display results in a compact format at the top"""
    # Clear screen to show results at top (works on most terminals)
    import os

    os.system("cls" if os.name == "nt" else "clear")

    print("🧪 LIQUID STATE ANALYSIS RESULTS 🧪")
    print("=" * 50)

    print(
        f"🔬 {results['liquid_name']} | 🌡️ {results['temperature']}°C | 📏 {results['pressure']} atm"
    )
    print(f"🏷️  STATE: {results['state']} | {results['description']}")

    # Show compact ASCII art of flask
    if results["flask_state"] == "frozen":
        flask_icon = "🧊 FROZEN: |❄️❄️❄️|"
    elif results["flask_state"] == "boiling":
        flask_icon = "🔥 BOILING: |💨💨💨|"
    else:
        flask_icon = "💧 LIQUID: |~~~~~|"

    print(f"🧪 Flask: {flask_icon}")

    print(
        f"📊 Freezing: {results['freezing_point']}°C | Boiling: {results['boiling_point_actual']}°C"
    )
    print("=" * 50)


def get_user_input():
    """Get input from user with simple prompts"""
    print("\n🎯 Let's analyze a liquid state!")
    print("🧪 The flask will show: STILL (liquid), FROZEN (solid), or BOILING (gas)")
    print()

    # Create analyzer instance
    analyzer = LiquidAnalyzer()
    liquids = analyzer.get_available_liquids()

    # Show available liquids
    print("📋 Available liquids:")
    liquid_list = list(liquids.keys())
    for i, liquid_key in enumerate(liquid_list, 1):
        liquid_info = liquids[liquid_key]
        print(f"   {i}. {liquid_info['name']}")

    # Get liquid choice
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

    # Get temperature
    while True:
        try:
            temperature = float(input("🌡️  Enter temperature in Celsius: "))
            break
        except ValueError:
            print("❌ Please enter a valid number")

    # Get pressure with default
    while True:
        try:
            pressure_input = input(
                "📏 Enter atmospheric pressure in atm (press Enter for 1.0): "
            )
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


def open_web_interface():
    """Open the web interface in browser"""
    if os.path.exists("index.html"):
        print("🌐 Opening web interface...")
        webbrowser.open("index.html")
    else:
        print("⚠️  Web interface (index.html) not found")


def main():
    """Main program function"""
    try:
        print("🧪 Welcome to Liquid State Analyzer - Coach Version!")
        print("=" * 50)

        # Create analyzer
        analyzer = LiquidAnalyzer()

        # Ask if they want to open web interface
        web_choice = input("\n🌐 Open web interface? (y/n): ").lower()
        if web_choice == "y":
            open_web_interface()

        while True:
            # Get user input
            temperature, pressure, liquid_type = get_user_input()

            # Perform analysis (remove delay and loading message)
            results = analyzer.analyze_liquid_state(temperature, pressure, liquid_type)

            # Display results (now shows at top)
            display_results(results)

            # Create web results
            analyzer.create_web_results(results)

            # Ask to save results (more compact)
            save_choice = input("\n💾 Save results? (y/n): ").lower()
            if save_choice == "y":
                analyzer.save_analysis_result(results)

            # Ask to continue (more compact)
            continue_choice = input("🔄 Analyze another? (y/n): ").lower()
            if continue_choice != "y":
                print("\n🎉 Thanks for using Liquid State Analyzer!")
                break

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as error:
        print(f"\n❌ Error: {error}")


# Run the program
if __name__ == "__main__":
    main()

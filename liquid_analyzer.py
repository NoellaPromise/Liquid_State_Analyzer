# Import libraries we need
import json  # For reading and writing JSON files
import os  # For checking if files exist

class LiquidAnalyzer:
    """This class analyzes liquid states - it's like a smart calculator for liquids"""
    
    def __init__(self):
        """This function runs when we create a new LiquidAnalyzer"""
        # Load liquid data from JSON file when analyzer starts
        self.liquids_data = self.load_liquids_data()
    
    def load_liquids_data(self):
        """This function loads liquid information from a JSON file"""
        try:
            # Try to open and read the liquids data file
            with open('liquids_data.json', 'r') as file:
                data = json.load(file)  # Convert JSON text to Python dictionary
                return data
        except FileNotFoundError:
            # If file doesn't exist, create it with default data
            print("📄 Creating liquids_data.json file...")
            default_data = self.get_default_liquids()  # Get default liquid data
            self.save_liquids_data(default_data)  # Save it to file
            return default_data
    
    def get_default_liquids(self):
        """This function returns the default liquid data"""
        return {
            "water": {
                "name": "Water (H₂O)",
                "freezing_point": 0.0,
                "boiling_point": 100.0
            },
            "ethanol": {
                "name": "Ethanol (C₂H₅OH)", 
                "freezing_point": -114.1,
                "boiling_point": 78.4
            },
            "mercury": {
                "name": "Mercury (Hg)",
                "freezing_point": -38.8,
                "boiling_point": 356.7
            },
            "nitrogen": {
                "name": "Nitrogen (N₂)",
                "freezing_point": -210.0,
                "boiling_point": -195.8
            },
            "oxygen": {
                "name": "Oxygen (O₂)",
                "freezing_point": -218.8,
                "boiling_point": -183.0
            }
        }
    
    def save_liquids_data(self, data):
        """This function saves liquid data to a JSON file"""
        with open('liquids_data.json', 'w') as file:
            # Convert Python dictionary to JSON text and save it
            json.dump(data, file, indent=2)  # indent=2 makes it look nice
    
    def get_available_liquids(self):
        """This function returns a list of available liquids for the dropdown"""
        # Create a new dictionary with just the names
        liquid_names = {}
        for key, liquid_info in self.liquids_data.items():
            liquid_names[key] = liquid_info['name']  # key = 'water', name = 'Water (H₂O)'
        return liquid_names
    
    def calculate_pressure_effect(self, base_boiling_point, pressure):
        """This function calculates how pressure changes boiling point"""
        # Simple formula: each 1 atm change affects boiling by 10°C
        pressure_difference = pressure - 1.0  # 1.0 atm is normal pressure
        adjusted_boiling = base_boiling_point + (pressure_difference * 10.0)
        return adjusted_boiling
    
    def analyze_liquid_state(self, temperature, pressure, liquid_type):
        """This is the main function that analyzes what state the liquid is in"""
        
        # Check if the liquid exists in our data
        if liquid_type not in self.liquids_data:
            raise ValueError(f"Unknown liquid: {liquid_type}")
        
        # Check if pressure makes sense
        if pressure <= 0:
            raise ValueError("Pressure must be greater than 0")
        
        # Get information about this liquid
        liquid = self.liquids_data[liquid_type]
        freezing_point = liquid["freezing_point"]  # When it freezes
        base_boiling_point = liquid["boiling_point"]  # When it boils at normal pressure
        
        # Calculate actual boiling point considering pressure
        actual_boiling_point = self.calculate_pressure_effect(base_boiling_point, pressure)
        
        # Decide what state the liquid is in
        if temperature <= freezing_point:
            # Temperature is at or below freezing point = SOLID
            state = "SOLID"
            flask_state = "frozen"  # How flask should look
            description = f"The liquid is FROZEN because {temperature}°C is at or below freezing point ({freezing_point}°C)"
            
        elif temperature >= actual_boiling_point:
            # Temperature is at or above boiling point = GAS
            state = "GAS"
            flask_state = "boiling"  # How flask should look
            description = f"The liquid is BOILING because {temperature}°C is at or above boiling point ({actual_boiling_point:.1f}°C)"
            
        else:
            # Temperature is between freezing and boiling = LIQUID
            state = "LIQUID"
            flask_state = "still"  # How flask should look
            description = f"The liquid is in normal LIQUID state"
        
        # Return all the information as a dictionary
        return {
            "liquid_name": liquid["name"],  # Full name like "Water (H₂O)"
            "temperature": temperature,  # Input temperature
            "pressure": pressure,  # Input pressure
            "state": state,  # SOLID, LIQUID, or GAS
            "flask_state": flask_state,  # frozen, still, or boiling (for frontend)
            "description": description,  # Explanation of why
            "freezing_point": freezing_point,  # Reference freezing point
            "boiling_point_normal": base_boiling_point,  # Normal boiling point
            "boiling_point_actual": round(actual_boiling_point, 1)  # Actual boiling point with pressure
        }
    
    def save_analysis_result(self, results):
        """This function saves analysis results to a file"""
        # Add timestamp to results
        import datetime  # Import datetime library
        results_with_time = results.copy()  # Make a copy
        results_with_time['analysis_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Load existing results if file exists
        if os.path.exists('analysis_results.json'):
            with open('analysis_results.json', 'r') as file:
                all_results = json.load(file)  # Load existing results
        else:
            all_results = []  # Start with empty list
        
        # Add new result to list
        all_results.append(results_with_time)
        
        # Save updated list back to file
        with open('analysis_results.json', 'w') as file:
            json.dump(all_results, file, indent=2)
        
        print("✅ Analysis result saved to analysis_results.json")

# Test the analyzer if this file is run directly
if __name__ == "__main__":
    print("🧪 Testing Liquid Analyzer...")
    
    # Create analyzer
    analyzer = LiquidAnalyzer()
    
    # Test with water at room temperature
    try:
        result = analyzer.analyze_liquid_state(25.0, 1.0, "water")
        print("Test successful!")
        print(f"State: {result['state']}")
        print(f"Description: {result['description']}")
    except Exception as error:
        print(f"Test failed: {error}")
# Import the libraries we need
from flask import Flask, request, jsonify  # Flask for web server, request for getting data, jsonify for sending JSON
from flask_cors import CORS  # CORS allows frontend to talk to backend
import json  # For working with JSON files
from liquid_analyzer import LiquidAnalyzer  # Import our main analyzer class

# Create a Flask web application
app = Flask(__name__)

# Enable CORS so frontend can connect to backend
CORS(app)

# Create an instance of our liquid analyzer
analyzer = LiquidAnalyzer()

# Route to serve the main HTML page
@app.route('/')
def home():
    """This function runs when someone visits the main page"""
    try:
        # Try to open and read the HTML file
        with open('index.html', 'r') as file:
            return file.read()
    except FileNotFoundError:
        # If HTML file doesn't exist, show this message
        return "<h1>Please save index.html in the same folder as this server!</h1>"

# API route to get list of available liquids
@app.route('/api/liquids', methods=['GET'])
def get_liquids():
    """This function returns all available liquids"""
    try:
        # Get liquids from our analyzer
        liquids = analyzer.get_available_liquids()
        # Send successful response with liquids data
        return jsonify({
            'success': True,
            'liquids': liquids
        })
    except Exception as error:
        # If something goes wrong, send error message
        return jsonify({
            'success': False,
            'error': str(error)
        }), 500

# API route to analyze liquid state
@app.route('/api/analyze', methods=['POST'])
def analyze_liquid():
    """This function analyzes the liquid state and returns results"""
    try:
        # Get JSON data from the frontend request
        data = request.get_json()
        
        # Extract the values we need
        temperature = float(data['temperature'])  # Convert to number
        pressure = float(data['pressure'])  # Convert to number
        liquid_type = data['liquid']  # Keep as text
        
        # Use our analyzer to check the liquid state
        results = analyzer.analyze_liquid_state(temperature, pressure, liquid_type)
        
        # Send successful response with analysis results
        return jsonify({
            'success': True,
            'results': results
        })
        
    except ValueError as error:
        # If user input is invalid, send error message
        return jsonify({
            'success': False,
            'error': str(error)
        }), 400
        
    except Exception as error:
        # If something else goes wrong, send error message
        return jsonify({
            'success': False,
            'error': f'Server error: {str(error)}'
        }), 500

# API route to check if server is working
@app.route('/api/health', methods=['GET'])
def health_check():
    """This function checks if the server is running properly"""
    return jsonify({
        'status': 'healthy',
        'message': 'Liquid State Analyzer server is running!'
    })

# Main code that runs when this file is executed
if __name__ == '__main__':
    print("🧪 Starting Liquid State Analyzer Server...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("📱 Frontend will connect to this backend automatically")
    print("🛑 Press Ctrl+C to stop the server")
    print("")
    
    # Start the Flask server
    # debug=True means it will restart when we change code
    # host='0.0.0.0' means it accepts connections from anywhere
    # port=5000 means it runs on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
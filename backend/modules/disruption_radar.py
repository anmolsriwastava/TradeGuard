import json
import requests
import os
from datetime import datetime
from typing import Dict, Tuple
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

class DisruptionRadar:
    
    def __init__(self):
        # Get API key from environment
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY', '')
        
        # Load mock data as fallback
        try:
            with open('data/mock_corridor_risk.json', 'r') as f:
                self.corridor_data = json.load(f)
        except:
            self.corridor_data = {"corridors": []}
    
    def fetch_weather_risk(self, port_code: str) -> int:
        """Get real weather data for a port"""
        
        # If no API key, use mock data
        if not self.weather_api_key or self.weather_api_key == '':
            print("No API key found, using mock weather data")
            return 45
        
        # Map port codes to city names
        port_to_city = {
            "INNSA": "Mumbai",
            "AEJEA": "Dubai", 
            "NLRTM": "Rotterdam",
            "SG SIN": "Singapore",
            "EGSZK": "Suez"
        }
        
        city = port_to_city.get(port_code, "Mumbai")
        
        try:
            # Call OpenWeatherMap API
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                wind_speed = data.get('wind', {}).get('speed', 0)
                weather_main = data.get('weather', [{}])[0].get('main', '')
                
                print(f"Weather in {city}: Wind {wind_speed} m/s, Condition: {weather_main}")
                
                # Convert wind speed to risk score
                if weather_main in ['Storm', 'Cyclone', 'Hurricane']:
                    return 95
                elif wind_speed > 20:  # Strong wind (72 km/h+)
                    return 85
                elif wind_speed > 15:  # Moderate wind (54 km/h+)
                    return 65
                elif wind_speed > 10:  # Light wind (36 km/h+)
                    return 40
                else:
                    return 15
            else:
                print(f"Weather API error: {response.status_code}")
                return 45
                
        except Exception as e:
            print(f"Weather API failed: {e}")
            return 45
    
    def compute_composite_risk(self, origin: str, destination: str) -> Tuple[int, str]:
        """Get real-time risk score using live weather data"""
        
        # Get real weather data
        weather_score = self.fetch_weather_risk(origin)
        
        # Find corridor in mock data for other components
        corridor_id = f"{origin}-{destination}"
        mock_data = None
        
        for corridor in self.corridor_data.get('corridors', []):
            if corridor['corridor_id'] == corridor_id:
                mock_data = corridor
                break
        
        if mock_data:
            ais_score = mock_data['components'].get('ais_score', 50)
            freight_score = mock_data['components'].get('freight_score', 50)
            nlp_score = mock_data['components'].get('nlp_score', 50)
        else:
            ais_score = 50
            freight_score = 50
            nlp_score = 50
        
        # Composite score (with weather now real!)
        risk_score = (0.35 * ais_score + 
                      0.20 * weather_score + 
                      0.20 * freight_score + 
                      0.25 * nlp_score)
        
        risk_score = int(risk_score)
        
        if risk_score < 30:
            risk_level = "LOW"
        elif risk_score < 65:
            risk_level = "MEDIUM"
        elif risk_score < 85:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        print(f"Risk Score: {risk_score} ({risk_level}) - Weather contribution: {weather_score}")
        
        return risk_score, risk_level
    
    def scan_all_corridors(self, shipments: list) -> list:
        """Scan all active shipments for disruptions"""
        affected = []
        
        for shipment in shipments:
            risk_score, risk_level = self.compute_composite_risk(
                shipment['origin_port'], 
                shipment['destination_port']
            )
            
            if risk_level in ["HIGH", "CRITICAL"]:
                affected.append({
                    "shipment": shipment,
                    "risk_score": risk_score,
                    "risk_level": risk_level
                })
        
        return affected
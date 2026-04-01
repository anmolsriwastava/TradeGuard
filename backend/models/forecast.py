import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

# Simple time series forecasting without heavy dependencies
# (Prophet requires additional setup, so we'll use a lightweight approach)

class RiskForecaster:
    def __init__(self):
        self.history_file = "backend/data/risk_history.json"
        self.load_history()
    
    def load_history(self):
        """Load historical risk scores"""
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        except:
            # Create sample historical data
            self.history = self.generate_sample_history()
            self.save_history()
    
    def generate_sample_history(self):
        """Generate sample historical data for demo"""
        history = []
        today = datetime.now()
        
        # Generate last 30 days of data with some pattern
        for i in range(30, -1, -1):
            date = today - timedelta(days=i)
            
            # Create pattern: low risk, then spike, then decline
            if i < 5:  # Last 5 days - high risk
                risk = 75 + np.random.randint(-10, 10)
            elif i < 10:  # 5-10 days ago - rising
                risk = 50 + (10 - i) * 5 + np.random.randint(-5, 5)
            elif i < 20:  # 10-20 days ago - medium
                risk = 40 + np.random.randint(-15, 15)
            else:  # 20-30 days ago - low
                risk = 25 + np.random.randint(-10, 10)
            
            history.append({
                "date": date.strftime("%Y-%m-%d"),
                "risk_score": min(max(risk, 0), 100)
            })
        
        return history
    
    def save_history(self):
        """Save risk history to file"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_current_risk(self, current_risk):
        """Add today's risk score to history"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if today already exists
        existing = [h for h in self.history if h["date"] == today]
        if not existing:
            self.history.append({
                "date": today,
                "risk_score": current_risk
            })
            # Keep last 30 days only
            self.history = self.history[-30:]
            self.save_history()
    
    def forecast(self, days=7):
        """
        Simple moving average + trend forecasting
        Returns forecasted risk scores for next 'days'
        """
        if len(self.history) < 7:
            return [50] * days
        
        # Get last 7 days of risk scores
        recent = self.history[-7:]
        recent_scores = [h["risk_score"] for h in recent]
        
        # Calculate trend (simple linear regression)
        x = list(range(len(recent_scores)))
        y = recent_scores
        
        # Calculate slope and intercept
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        # Slope
        if n * sum_x2 - sum_x ** 2 != 0:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        else:
            slope = 0
        
        # Intercept
        intercept = (sum_y - slope * sum_x) / n
        
        # Forecast next 'days'
        forecasts = []
        for i in range(1, days + 1):
            forecast = intercept + slope * (n + i - 1)
            forecasts.append(min(max(forecast, 0), 100))
        
        return forecasts
    
    def get_trend(self):
        """Determine if risk is increasing, decreasing, or stable"""
        if len(self.history) < 7:
            return "stable"
        
        recent = self.history[-7:]
        scores = [h["risk_score"] for h in recent]
        
        # Compare last 3 days vs previous 4 days
        recent_avg = sum(scores[-3:]) / 3
        previous_avg = sum(scores[:4]) / 4
        
        if recent_avg > previous_avg + 5:
            return "increasing"
        elif recent_avg < previous_avg - 5:
            return "decreasing"
        else:
            return "stable"
    
    def get_risk_alert(self, forecast_risk):
        """Generate alert based on forecasted risk"""
        if forecast_risk >= 80:
            return "CRITICAL ALERT: High risk expected in coming days. Prepare contingency plans now."
        elif forecast_risk >= 60:
            return "WARNING: Risk increasing. Monitor closely and review alternatives."
        elif forecast_risk >= 40:
            return "CAUTION: Moderate risk expected. Stay informed."
        else:
            return "NORMAL: Risk levels expected to remain low."


# For testing
if __name__ == "__main__":
    forecaster = RiskForecaster()
    print("Risk History:")
    for h in forecaster.history[-7:]:
        print(f"  {h['date']}: {h['risk_score']}")
    
    forecasts = forecaster.forecast(7)
    print("\n7-Day Forecast:")
    for i, f in enumerate(forecasts, 1):
        print(f"  Day {i}: {f:.0f}")
    
    print(f"\nTrend: {forecaster.get_trend()}")
    print(f"Alert: {forecaster.get_risk_alert(forecasts[0])}")
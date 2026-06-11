import math

class RelayTestingEngine:
    def calculate(self, pickup_current_amps: float, fault_current_amps: float, time_dial_setting: float, curve_type: str = "Extremely Inverse") -> dict:
        """
        Calculates protection relay trip times based on standard IEEE Overcurrent curves.
        """
        try:
            # Current multiplier (M)
            m = fault_current_amps / pickup_current_amps
            
            if m <= 1.0:
                return {
                    "status": "success",
                    "result": "> **[STANDBY] RELAY ANALYSIS**\nFault current is below pickup. Relay will not trip.",
                    "chart_data": None
                }
                
            # IEEE constants for Ext. Inverse: A=28.2, B=0.1217, p=2.0
            # For standard Inverse: A=0.14, B=0, p=0.02
            # Simplified generic calculation for demonstration
            if curve_type.lower() == "extremely inverse":
                a, b, p = 28.2, 0.1217, 2.0
            elif curve_type.lower() == "very inverse":
                a, b, p = 19.61, 0.491, 2.0
            else: # Standard Inverse
                a, b, p = 0.0515, 0.114, 0.02
                
            # Trip time t = TDS * (A / (M^p - 1) + B)
            trip_time_seconds = time_dial_setting * (a / (math.pow(m, p) - 1) + b)
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Relay Trip Time (s)"],
                    "datasets": [{
                        "label": f"IEEE {curve_type} Clearance",
                        "data": [round(trip_time_seconds, 3)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[TRIP SIMULATION] RELAY COORDINATION**\n"
                    f"- **Curve**: IEEE {curve_type}\n"
                    f"- **Fault Magnitude (M)**: {round(m, 2)}x Pickup\n"
                    f"- **Calculated Clearance Time**: {round(trip_time_seconds, 3)} Seconds\n"
                    f"Warning: Ensure downstream breakers trip faster than {round(trip_time_seconds, 3)}s to maintain selectivity."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Relay calculation failed: {str(e)}"}

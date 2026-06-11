import math

class WindAerodynamicsEngine:
    def calculate(self, rotor_diameter_m: float, wind_speed_m_s: float, air_density: float = 1.225, cp_coefficient: float = 0.45) -> dict:
        """
        Calculates extractable wind power based on Betz's Law and rotor sweep area.
        """
        try:
            radius = rotor_diameter_m / 2
            swept_area = math.pi * (radius ** 2)
            
            # P = 0.5 * rho * A * v^3 * Cp
            power_watts = 0.5 * air_density * swept_area * (wind_speed_m_s ** 3) * cp_coefficient
            power_mw = power_watts / 1_000_000
            
            betz_limit_mw = (0.5 * air_density * swept_area * (wind_speed_m_s ** 3) * 0.593) / 1_000_000
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Actual Power (MW)", "Betz Limit (MW)"],
                    "datasets": [{
                        "label": "Wind Turbine Aerodynamic Power",
                        "data": [round(power_mw, 2), round(betz_limit_mw, 2)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] WIND TURBINE AERODYNAMICS**\n"
                    f"- **Rotor Swept Area**: {round(swept_area, 1)} m²\n"
                    f"- **Wind Speed**: {wind_speed_m_s} m/s\n"
                    f"- **Extractable Mechanical Power**: {round(power_mw, 2)} MW\n"
                    f"- **Theoretical Betz Limit**: {round(betz_limit_mw, 2)} MW\n"
                    f"Aero-efficiency (Cp) set to {cp_coefficient}."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Wind Aerodynamics calculation failed: {str(e)}"}

class EVFleetChargingEngine:
    def calculate(self, number_of_buses: int, battery_capacity_kwh: float, charging_window_hours: float, charger_efficiency: float = 0.92) -> dict:
        """
        Calculates peak load requirements for heavy-duty EV fleet charging (e.g., transit buses or semi-trucks).
        """
        try:
            total_energy_kwh = number_of_buses * battery_capacity_kwh
            energy_from_grid = total_energy_kwh / charger_efficiency
            
            # Peak power required if all charge simultaneously uniformly
            peak_power_kw = energy_from_grid / charging_window_hours
            peak_power_mw = peak_power_kw / 1000
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Fleet Energy (kWh)", "Grid Energy Req (kWh)", "Peak Demand (kW)"],
                    "datasets": [{
                        "label": "EV Fleet Depot Requirements",
                        "data": [total_energy_kwh, energy_from_grid, peak_power_kw]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] EV FLEET CHARGING PROFILER**\n"
                    f"- **Fleet Size**: {number_of_buses} vehicles\n"
                    f"- **Total Daily Energy**: {round(energy_from_grid, 2)} kWh\n"
                    f"- **Required Peak Coincident Demand**: {round(peak_power_mw, 2)} MW\n"
                    f"- **Infrastructure**: Ensure grid connection and transformers can handle {round(peak_power_mw * 1.2, 2)} MVA (including 20% margin)."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"EV Fleet calculation failed: {str(e)}"}

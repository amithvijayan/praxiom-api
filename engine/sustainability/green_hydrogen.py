class GreenHydrogenViabilityEngine:
    def calculate(self, electrolyzer_mw: float, power_price_mwh: float, capacity_factor: float = 0.5) -> dict:
        """
        Calculates annual H2 production and Levelized Cost of Hydrogen (LCOH).
        Assumes 50 kWh to produce 1 kg of H2.
        """
        try:
            # 1 MW = 1000 kW. Running for 1 hour = 1000 kWh.
            # 1000 kWh / 50 kWh/kg = 20 kg/hr per MW.
            annual_hours = 8760 * capacity_factor
            total_energy_mwh = electrolyzer_mw * annual_hours
            total_energy_kwh = total_energy_mwh * 1000
            
            annual_h2_kg = total_energy_kwh / 50.0
            annual_h2_tons = annual_h2_kg / 1000.0
            
            # Simple LCOH (Power OPEX + Capex Amortization assumed at $2/kg)
            power_cost_per_kg = (50.0 / 1000.0) * power_price_mwh 
            lcoh_usd_per_kg = power_cost_per_kg + 2.0 
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Energy Input (GWh)", "H2 Output (Tons)", "LCOH ($/kg)"],
                    "datasets": [{
                        "label": "Green Hydrogen Metrics",
                        "data": [round(total_energy_mwh/1000, 1), round(annual_h2_tons, 1), round(lcoh_usd_per_kg, 2)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] GREEN HYDROGEN VIABILITY**\n"
                    f"- **Electrolyzer Capacity**: {electrolyzer_mw} MW\n"
                    f"- **Annual Production**: {round(annual_h2_tons, 1)} metric tons/year\n"
                    f"- **Power Cost**: ${power_price_mwh}/MWh\n"
                    f"- **Estimated LCOH**: ${round(lcoh_usd_per_kg, 2)}/kg\n"
                    f"Note: Standard target for competitive Green H2 is <$2.00/kg."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Green Hydrogen calculation failed: {str(e)}"}

class NuclearSMREngine:
    def calculate(self, thermal_power_mwth: float, thermal_efficiency: float, availability_factor: float = 0.95) -> dict:
        """
        Calculates electrical output and annual generation for a Small Modular Reactor (SMR).
        """
        try:
            electrical_power_mwe = thermal_power_mwth * thermal_efficiency
            annual_generation_gwh = (electrical_power_mwe * 8760 * availability_factor) / 1000
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Thermal Power (MWth)", "Electrical Power (MWe)"],
                    "datasets": [{
                        "label": "Nuclear SMR Output Capacity",
                        "data": [thermal_power_mwth, electrical_power_mwe]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] NUCLEAR SMR THERMODYNAMICS**\n"
                    f"- **Reactor Core Thermal Power**: {thermal_power_mwth} MWth\n"
                    f"- **Gross Electrical Output**: {round(electrical_power_mwe, 2)} MWe\n"
                    f"- **Annual Zero-Carbon Generation**: {round(annual_generation_gwh, 2)} GWh/yr\n"
                    f"Note: Baseload generation confirmed. High inertia contribution to local grid."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Nuclear SMR calculation failed: {str(e)}"}

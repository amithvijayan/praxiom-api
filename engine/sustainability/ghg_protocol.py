from engine.registry import EngineRegistry

@EngineRegistry.register("ghg_scope2")
class GhgProtocolEngine:
    """
    Deterministic GHG Protocol Scope 2 Emissions Engine.
    Calculates indirect emissions from purchased electricity.
    """
    def calculate(self, electricity_mwh: float, grid_emission_factor: float = 0.45) -> dict:
        """
        Calculates Scope 2 emissions based on MWh consumed and the regional grid emission factor (tCO2e/MWh).
        """
        total_tco2e = electricity_mwh * grid_emission_factor
        
        chart_data = [
            {"name": "Electricity (MWh)", "value": electricity_mwh},
            {"name": "Scope 2 Emissions (tCO2e)", "value": round(total_tco2e, 2)}
        ]

        text_result = (
            f"Sustainability Physics Output: Consuming {electricity_mwh} MWh of electricity "
            f"on a grid with an emission factor of {grid_emission_factor} tCO2e/MWh results "
            f"in {round(total_tco2e, 2)} metric tons of CO2 equivalent (Scope 2)."
        )

        return {
            "result_text": text_result,
            "chart_data": chart_data
        }

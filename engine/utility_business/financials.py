from engine.registry import EngineRegistry

@EngineRegistry.register("lcoe_financials")
class LcoeEngine:
    """
    Deterministic Levelized Cost of Energy (LCOE) Engine.
    Calculates the per-MWh cost of a power plant over its lifetime.
    """
    def calculate(self, capex: float, opex_annual: float, annual_generation_mwh: float, lifespan_years: int = 20, discount_rate: float = 0.08) -> dict:
        """
        Calculates LCOE using standardized discount formulas.
        """
        total_discounted_cost = capex
        total_discounted_generation = 0.0

        for year in range(1, lifespan_years + 1):
            discount_factor = (1 + discount_rate) ** year
            total_discounted_cost += opex_annual / discount_factor
            total_discounted_generation += annual_generation_mwh / discount_factor

        lcoe = total_discounted_cost / total_discounted_generation
        
        chart_data = [
            {"name": "CAPEX ($)", "value": capex},
            {"name": f"Total OPEX over {lifespan_years}y ($)", "value": round(opex_annual * lifespan_years, 2)},
            {"name": "LCOE ($/MWh)", "value": round(lcoe, 2)}
        ]

        text_result = (
            f"Utility Economics Output: For a plant with ${capex} CAPEX, ${opex_annual}/yr OPEX, "
            f"generating {annual_generation_mwh} MWh/yr over {lifespan_years} years at an {discount_rate*100}% discount rate, "
            f"the Levelized Cost of Energy (LCOE) is strictly ${round(lcoe, 2)} per MWh."
        )

        return {
            "result_text": text_result,
            "chart_data": chart_data
        }

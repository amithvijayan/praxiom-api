from engine.registry import EngineRegistry

@EngineRegistry.register("bess_sizing")
class BessSizingEngine:
    """
    Deterministic Battery Energy Storage System (BESS) Sizing Engine.
    Zero hallucination allowed. Strict physics only.
    """
    def calculate(self, load_mw: float, duration_hours: float, dod_percentage: float = 80.0, rte_percentage: float = 85.0) -> dict:
        """
        Calculates the required physical Nameplate Capacity of a BESS based on load and losses.
        """
        # Convert percentages
        dod = dod_percentage / 100.0
        rte = rte_percentage / 100.0
        
        # Physics formulas
        usable_energy_mwh = load_mw * duration_hours
        nameplate_energy_mwh = usable_energy_mwh / (dod * rte)
        
        # Construct exact chart data for UI
        chart_data = [
            {"name": "Usable Energy (MWh)", "value": round(usable_energy_mwh, 2)},
            {"name": "Nameplate Required (MWh)", "value": round(nameplate_energy_mwh, 2)},
            {"name": "Losses/Reserve (MWh)", "value": round(nameplate_energy_mwh - usable_energy_mwh, 2)}
        ]

        text_result = (
            f"BESS Physics Output: To support a {load_mw}MW load for {duration_hours} hours "
            f"with an {dod_percentage}% Depth of Discharge and {rte_percentage}% Round Trip Efficiency, "
            f"the required Nameplate Capacity is {round(nameplate_energy_mwh, 2)} MWh."
        )

        return {
            "result_text": text_result,
            "chart_data": chart_data
        }

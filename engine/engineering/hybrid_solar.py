class HybridSolarEngine:
    def calculate(self, array_capacity_kw: float, irradiation_kwh_m2: float, has_bess: bool, is_grid_tied: bool) -> dict:
        """
        Evaluates yield for Online (Grid-tied), Offline (Off-grid), or Hybrid solar systems.
        """
        try:
            system_loss_factor = 0.85 if is_grid_tied else 0.75 # Higher losses for off-grid due to battery cyclic losses
            daily_yield_kwh = array_capacity_kw * irradiation_kwh_m2 * system_loss_factor
            
            sys_type = "HYBRID" if (is_grid_tied and has_bess) else ("OFF-GRID" if not is_grid_tied else "GRID-TIED")
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Array Capacity (kW)", "Daily Yield (kWh)"],
                    "datasets": [{
                        "label": f"{sys_type} Solar Performance",
                        "data": [array_capacity_kw, round(daily_yield_kwh, 2)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] {sys_type} SOLAR TOPOLOGY ANALYSIS**\n"
                    f"- **Array Size**: {array_capacity_kw} kWp\n"
                    f"- **Solar Insolation**: {irradiation_kwh_m2} Peak Sun Hours\n"
                    f"- **Estimated Daily Yield**: {round(daily_yield_kwh, 2)} kWh/day\n"
                    f"- **System Efficiency**: {system_loss_factor * 100}%\n"
                    f"Status: Ready for detailed hourly simulation."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Hybrid Solar calculation failed: {str(e)}"}

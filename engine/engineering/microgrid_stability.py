class MicrogridStabilityEngine:
    def calculate(self, load_mw: float, pv_mw: float, bess_mw: float, diesel_mw: float) -> dict:
        """
        Calculates microgrid islanding stability and synthetic inertia adequacy.
        """
        try:
            total_generation = pv_mw + bess_mw + diesel_mw
            inertia_ratio = (diesel_mw + (bess_mw * 0.5)) / load_mw # Assuming BESS provides 50% synthetic inertia effectiveness compared to spinning mass
            
            if total_generation < load_mw:
                status = "WARNING"
                msg = "Generation deficit. Load shedding required during islanding."
            elif inertia_ratio < 0.2:
                status = "WARNING"
                msg = "Critically low inertia. High RoCoF (Rate of Change of Frequency) expected during transients. Increase BESS synthetic inertia or diesel spinning reserve."
            else:
                status = "PASS"
                msg = "Microgrid stability robust. Synthetic inertia adequate."
                
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Load", "PV", "BESS", "Diesel"],
                    "datasets": [{
                        "label": "Microgrid Dispatch Profile (MW)",
                        "data": [load_mw, pv_mw, bess_mw, diesel_mw]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[{status}] MICROGRID STABILITY ANALYSIS**\n"
                    f"- **Total Load**: {load_mw} MW\n"
                    f"- **Total Generation**: {total_generation} MW\n"
                    f"- **Inertial Adequacy Ratio**: {round(inertia_ratio * 100, 1)}%\n"
                    f"- **Verdict**: {msg}"
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Stability calculation failed: {str(e)}"}

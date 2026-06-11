import math

class PowerQualityHarmonicsEngine:
    def calculate(self, fundamental_current: float, harmonic_currents: list[float]) -> dict:
        """
        Calculates Total Harmonic Distortion (THD) and identifies active filter requirements.
        """
        try:
            sum_sq_harmonics = sum([i**2 for i in harmonic_currents])
            thd_i = (math.sqrt(sum_sq_harmonics) / fundamental_current) * 100
            
            compliance = "PASS" if thd_i <= 5.0 else "WARNING"
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Fundamental"] + [f"H{i+2}" for i in range(len(harmonic_currents))],
                    "datasets": [{
                        "label": "Harmonic Spectrum (Amps)",
                        "data": [fundamental_current] + harmonic_currents
                    }]
                }
            }
            
            result_str = (
                f"> **[{compliance}] IEEE 519 HARMONIC ANALYSIS**\n"
                f"- **Fundamental Current**: {fundamental_current} A\n"
                f"- **Total Harmonic Distortion (THDi)**: {round(thd_i, 2)}%\n"
            )
            
            if thd_i > 5.0:
                filter_size = math.sqrt(sum_sq_harmonics) * 1.2 # 20% margin
                result_str += f"\n- **Recommendation**: Active Harmonic Filter required. Minimum rating: {round(filter_size, 2)} A."
                
            return {
                "status": "success",
                "result": result_str,
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Harmonic calculation failed: {str(e)}"}

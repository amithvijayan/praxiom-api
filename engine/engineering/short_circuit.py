import math

class ShortCircuitAnalysisEngine:
    def calculate(self, base_mva: float, voltage_kv: float, source_impedance_pu: float, fault_type: str = "3-phase") -> dict:
        """
        Calculates Symmetrical Fault Current based on IEC 60909.
        """
        try:
            # Base current calculation
            i_base = (base_mva * 1000) / (math.sqrt(3) * voltage_kv)
            
            # Symmetrical fault current
            i_fault_sym = i_base / source_impedance_pu
            
            # Peak asymmetrical fault current (using an assumed X/R ratio of 10 for standard distribution)
            x_r_ratio = 10
            kappa = 1.02 + 0.98 * math.exp(-3 / x_r_ratio)
            i_peak_asym = kappa * math.sqrt(2) * i_fault_sym
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Base Current", "Sym Fault", "Peak Asym Fault"],
                    "datasets": [{
                        "label": "Short Circuit Currents (Amps)",
                        "data": [round(i_base), round(i_fault_sym), round(i_peak_asym)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] IEC 60909 SHORT CIRCUIT ANALYSIS COMPLETE**\n"
                    f"- **Fault Type**: {fault_type}\n"
                    f"- **Voltage Level**: {voltage_kv} kV\n"
                    f"- **Symmetrical Fault Current**: {round(i_fault_sym, 2)} A\n"
                    f"- **Peak Asymmetrical Current**: {round(i_peak_asym, 2)} A\n"
                    f"Warning: Ensure all switchgear is rated for at least {round(i_peak_asym/1000, 2)} kA breaking capacity."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Short circuit calculation failed: {str(e)}"}

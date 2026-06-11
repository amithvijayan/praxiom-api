class SubstationDesignEngine:
    def calculate(self, system_voltage_kv: float, mva_capacity: float, short_circuit_ka: float) -> dict:
        """
        Calculates physical clearances, busbar ampacity, and switchgear ratings for Air-Insulated Substations (AIS).
        """
        try:
            # 1. Busbar Ampacity Required
            # I = MVA / (sqrt(3) * kV)
            import math
            nominal_current = (mva_capacity * 1000) / (math.sqrt(3) * system_voltage_kv)
            
            # 2. IEC Minimum Clearances (Rule of thumb estimations)
            # Phase to Earth clearance (mm) ~ approx 10 * kV for low/medium, scaling up
            phase_to_earth_mm = system_voltage_kv * 10
            if system_voltage_kv >= 400: phase_to_earth_mm = 3500
            elif system_voltage_kv >= 220: phase_to_earth_mm = 2100
            elif system_voltage_kv >= 132: phase_to_earth_mm = 1300
            
            phase_to_phase_mm = phase_to_earth_mm * 1.15 # Approx 15% larger
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Ph-Earth (mm)", "Ph-Ph (mm)"],
                    "datasets": [{
                        "label": f"AIS Clearances at {system_voltage_kv}kV",
                        "data": [phase_to_earth_mm, round(phase_to_phase_mm)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] SUBSTATION AIS ENGINEERING**\n"
                    f"- **System Voltage**: {system_voltage_kv} kV\n"
                    f"- **Nominal Busbar Current**: {round(nominal_current, 1)} A\n"
                    f"- **Switchgear Short-Circuit Rating**: Must exceed {short_circuit_ka} kA (3-second withstand).\n"
                    f"- **Min Phase-to-Earth Clearance**: {phase_to_earth_mm} mm\n"
                    f"- **Min Phase-to-Phase Clearance**: {round(phase_to_phase_mm)} mm\n"
                    f"Note: Use rigid aluminum tubular busbars to withstand {short_circuit_ka}kA electromechanical forces."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Substation Design failed: {str(e)}"}

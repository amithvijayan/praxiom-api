class PowerEquipmentTestingEngine:
    def calculate(self, equipment_type: str, test_voltage_kv: float, measured_leakage_ma: float, dga_hydrogen_ppm: float = 0) -> dict:
        """
        Simulates high-voltage testing diagnostics (Hipot/Megger and DGA).
        """
        try:
            # Insulation Resistance / Leakage Current Check
            # ANSI/NETA standard rule of thumb: Hipot leakage should generally be under 5 mA for healthy XLPE cables/switchgear
            insulation_status = "PASS"
            if measured_leakage_ma > 5.0:
                insulation_status = "FAIL"
            elif measured_leakage_ma > 2.0:
                insulation_status = "WARNING"
                
            # DGA (Dissolved Gas Analysis) for Transformers
            dga_status = "N/A"
            dga_msg = ""
            if equipment_type.upper() == "TRANSFORMER":
                if dga_hydrogen_ppm > 100:
                    dga_status = "CRITICAL"
                    dga_msg = "High Hydrogen (H2) detected. Indicates partial discharge or low-energy arcing."
                elif dga_hydrogen_ppm > 50:
                    dga_status = "WARNING"
                    dga_msg = "Elevated Hydrogen (H2). Monitor closely."
                else:
                    dga_status = "NORMAL"
                    dga_msg = "Combustible gases within acceptable limits."
                    
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Measured Leakage (mA)", "Leakage Limit (mA)"],
                    "datasets": [{
                        "label": f"{equipment_type} Dielectric Integrity",
                        "data": [measured_leakage_ma, 5.0]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[TEST RESULTS] POWER EQUIPMENT DIAGNOSTICS**\n"
                    f"- **Equipment**: {equipment_type.upper()}\n"
                    f"- **Test Voltage applied**: {test_voltage_kv} kV DC\n"
                    f"- **Leakage Current**: {measured_leakage_ma} mA -> **{insulation_status}**\n"
                    + (f"- **DGA Analysis**: {dga_status}. {dga_msg}\n" if equipment_type.upper() == "TRANSFORMER" else "") +
                    f"Ensure equipment is properly grounded post-test to dissipate capacitive charge."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Equipment Testing failed: {str(e)}"}

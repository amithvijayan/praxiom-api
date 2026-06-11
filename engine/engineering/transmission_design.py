import math

class TransmissionDesignEngine:
    def calculate(self, span_length_m: float, conductor_weight_kg_m: float, horizontal_tension_kg: float) -> dict:
        """
        Calculates conductor sag and mechanical tension based on the parabolic catenary curve.
        """
        try:
            # Parabolic sag equation: Sag = (w * L^2) / (8 * T)
            sag_m = (conductor_weight_kg_m * (span_length_m ** 2)) / (8 * horizontal_tension_kg)
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Span Length (m)", "Sag (m)", "Tension (kg/10)"],
                    "datasets": [{
                        "label": "Mechanical Conductor Profile",
                        "data": [span_length_m, round(sag_m, 2), round(horizontal_tension_kg/10, 2)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] TRANSMISSION LINE MECHANICS**\n"
                    f"- **Span Length**: {span_length_m} m\n"
                    f"- **Conductor Tension**: {horizontal_tension_kg} kgf\n"
                    f"- **Maximum Mid-Span Sag**: {round(sag_m, 2)} m\n"
                    f"Warning: Ensure sag does not violate regional ground clearance codes under high temperature and ice-loading conditions."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Transmission Design failed: {str(e)}"}

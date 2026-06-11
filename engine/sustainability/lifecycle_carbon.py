class LifecycleCarbonAssessmentEngine:
    def calculate(self, material_mass_kg: float, transport_distance_km: float, operations_years: float, energy_per_year_kwh: float, grid_carbon_intensity_kg_kwh: float) -> dict:
        """
        Calculates Scope 1, 2, and 3 emissions for an energy asset over its lifecycle.
        """
        try:
            # Scope 3: Embodied Carbon (Manufacturing + Transport)
            # Assuming generic average: 5 kgCO2/kg for materials, 0.1 kgCO2/ton-km for transport
            material_emissions = material_mass_kg * 5.0
            transport_emissions = (material_mass_kg / 1000) * transport_distance_km * 0.1
            scope_3_kg = material_emissions + transport_emissions
            
            # Scope 2: Operational Electricity
            scope_2_kg = energy_per_year_kwh * grid_carbon_intensity_kg_kwh * operations_years
            
            # Total LCA
            total_lca_tons = (scope_2_kg + scope_3_kg) / 1000
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Scope 2 (Ops)", "Scope 3 (Supply Chain)", "Total LCA"],
                    "datasets": [{
                        "label": "Lifecycle Emissions (tCO2e)",
                        "data": [round(scope_2_kg/1000, 1), round(scope_3_kg/1000, 1), round(total_lca_tons, 1)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] LIFECYCLE CARBON ASSESSMENT (LCA)**\n"
                    f"- **Scope 2 (Operational)**: {round(scope_2_kg/1000, 1)} tCO2e\n"
                    f"- **Scope 3 (Embodied/Supply)**: {round(scope_3_kg/1000, 1)} tCO2e\n"
                    f"- **Total Lifecycle Impact**: {round(total_lca_tons, 1)} tCO2e over {operations_years} years.\n"
                    f"To achieve Net-Zero, you must offset this total tonnage."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"LCA calculation failed: {str(e)}"}

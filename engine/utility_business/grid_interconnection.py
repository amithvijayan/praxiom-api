class GridInterconnectionTariffEngine:
    def calculate(self, interconnection_mw: float, distance_to_substation_km: float, voltage_kv: float) -> dict:
        """
        Estimates interconnection capital costs based on capacity, distance, and transmission voltage.
        """
        try:
            # Base substation upgrade cost: $50,000 per MW
            substation_upgrade_cost = interconnection_mw * 50_000
            
            # Transmission line cost: Higher voltage = higher cost per km
            # 33kV: $100k/km, 132kV: $300k/km, 400kV: $800k/km
            cost_per_km = 100_000
            if voltage_kv >= 100:
                cost_per_km = 300_000
            if voltage_kv >= 300:
                cost_per_km = 800_000
                
            line_cost = distance_to_substation_km * cost_per_km
            
            total_capex = substation_upgrade_cost + line_cost
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Substation Upgrades ($)", "Transmission Line ($)", "Total Capex ($)"],
                    "datasets": [{
                        "label": "Grid Interconnection Tariff Estimator",
                        "data": [substation_upgrade_cost, line_cost, total_capex]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] GRID INTERCONNECTION ESTIMATOR**\n"
                    f"- **Capacity**: {interconnection_mw} MW at {voltage_kv} kV\n"
                    f"- **Distance**: {distance_to_substation_km} km\n"
                    f"- **Total Estimated Cost**: ${round(total_capex / 1_000_000, 2)} Million\n"
                    f"Warning: Does not include deep grid reinforcement costs or right-of-way land acquisition."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"Interconnection calculation failed: {str(e)}"}

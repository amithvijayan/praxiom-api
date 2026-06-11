class PowerPurchaseAgreementEngine:
    def calculate(self, annual_generation_mwh: float, strike_price_mwh: float, term_years: int, annual_escalator_pct: float = 2.0) -> dict:
        """
        Calculates cumulative revenue for a Power Purchase Agreement with an annual escalator.
        """
        try:
            total_revenue = 0.0
            yearly_revenues = []
            current_price = strike_price_mwh
            
            for year in range(1, term_years + 1):
                rev = annual_generation_mwh * current_price
                total_revenue += rev
                
                if year <= 10: # Only map the first 10 years for the chart to keep it clean
                    yearly_revenues.append(rev)
                    
                current_price *= (1 + (annual_escalator_pct / 100))
                
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": [f"Yr {i+1}" for i in range(len(yearly_revenues))],
                    "datasets": [{
                        "label": "Annual Revenue ($)",
                        "data": [round(r) for r in yearly_revenues]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] POWER PURCHASE AGREEMENT (PPA) MODEL**\n"
                    f"- **PPA Term**: {term_years} years\n"
                    f"- **Base Strike Price**: ${strike_price_mwh}/MWh\n"
                    f"- **Annual Escalator**: {annual_escalator_pct}%\n"
                    f"- **Total Cumulative Revenue**: ${round(total_revenue / 1_000_000, 2)} Million\n"
                    f"Contract structure is heavily backend-weighted due to the escalator."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"PPA calculation failed: {str(e)}"}

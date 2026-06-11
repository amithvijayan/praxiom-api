from engine.registry import EngineRegistry

@EngineRegistry.register("ppa_modeling")
class PPAModelingEngine:
    """
    Power Purchase Agreement (PPA) financial modeling. Calculates Net Present Value (NPV), 
    annual revenue, and total revenue over the contract life.
    """
    
    def calculate(
        self,
        annual_energy_mwh: float,
        starting_ppa_rate_usd_per_mwh: float,
        annual_escalation_rate_percentage: float = 2.0,
        contract_term_years: int = 20,
        discount_rate_percentage: float = 8.0
    ):
        escalation_factor = 1 + (annual_escalation_rate_percentage / 100)
        discount_factor = 1 + (discount_rate_percentage / 100)
        
        total_revenue = 0.0
        npv_revenue = 0.0
        
        # Simple straight-line energy delivery for the term
        for year in range(1, contract_term_years + 1):
            # Calculate current year's rate
            current_rate = starting_ppa_rate_usd_per_mwh * (escalation_factor ** (year - 1))
            
            # Calculate revenue for the year
            annual_rev = annual_energy_mwh * current_rate
            total_revenue += annual_rev
            
            # Discount back to present value
            npv_revenue += annual_rev / (discount_factor ** year)
            
        result_text = (
            f"Utility Business Output: For a {contract_term_years}-year PPA delivering {annual_energy_mwh} MWh annually, "
            f"starting at ${starting_ppa_rate_usd_per_mwh}/MWh with a {annual_escalation_rate_percentage}% escalation, "
            f"the total nominal revenue is ${total_revenue:,.2f}. "
            f"Discounted at {discount_rate_percentage}%, the Net Present Value (NPV) of revenue is ${npv_revenue:,.2f}."
        )
        
        chart_data = [
            {"name": "NPV Revenue ($)", "value": round(npv_revenue, 2)},
            {"name": "Nominal Future Value ($)", "value": round(total_revenue - npv_revenue, 2)}
        ]
        
        return {
            "result_text": result_text,
            "chart_data": chart_data
        }

from engine.registry import EngineRegistry

@EngineRegistry.register("carbon_tax_liability")
class CarbonTaxLiabilityEngine:
    """
    Calculates strict financial liabilities for GHG Scope 1 and Scope 2 emissions 
    based on regional carbon pricing standards (e.g., $USD/ton of CO2e).
    """
    
    def calculate(
        self,
        scope1_emissions_tons: float,
        scope2_emissions_tons: float,
        carbon_tax_rate_usd_per_ton: float = 50.0,
        free_allowance_tons: float = 0.0
    ):
        # 1. Total Emissions
        total_emissions = scope1_emissions_tons + scope2_emissions_tons
        
        # 2. Taxable Emissions (Emissions above the free allowance threshold)
        taxable_emissions = max(0.0, total_emissions - free_allowance_tons)
        
        # 3. Financial Liability
        total_liability_usd = taxable_emissions * carbon_tax_rate_usd_per_ton
        
        result_text = (
            f"Sustainability Output: Total Scope 1 & 2 emissions are {total_emissions} tons of CO2e. "
            f"With a free allowance of {free_allowance_tons} tons, the taxable emissions are {taxable_emissions} tons. "
            f"At a carbon tax rate of ${carbon_tax_rate_usd_per_ton}/ton, the total financial liability is ${total_liability_usd:,.2f} USD."
        )
        
        chart_data = [
            {"name": "Free Allowance (Tons)", "value": min(total_emissions, free_allowance_tons)},
            {"name": "Taxable Emissions (Tons)", "value": taxable_emissions}
        ]
        
        return {
            "result_text": result_text,
            "chart_data": chart_data
        }

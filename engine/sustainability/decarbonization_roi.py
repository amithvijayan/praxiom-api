from engine.registry import EngineRegistry
from engine.engineering.bess_sizing import BessSizingEngine
from engine.sustainability.carbon_tax_liability import CarbonTaxLiabilityEngine

@EngineRegistry.register("calculate_decarbonization_roi")
class DecarbonizationROI:
    """
    Mutual Operations Engine: Calculates the ROI of decarbonizing an industrial facility.
    It links the physical BESS engineering with the financial Carbon Tax liability.
    """
    def calculate(
        self,
        current_annual_emissions_tco2e: float,
        target_reduction_percentage: float,
        carbon_tax_rate_per_ton: float,
        solar_capex_per_mw: float,
        bess_capex_per_mwh: float,
        solar_capacity_factor: float = 0.20
    ):
        # 1. Target Emission Reduction
        emissions_to_reduce = current_annual_emissions_tco2e * (target_reduction_percentage / 100.0)
        
        # 2. Estimate Solar required
        grid_emission_factor_tco2_per_mwh = 0.5
        required_solar_mwh_yr = emissions_to_reduce / grid_emission_factor_tco2_per_mwh
        required_solar_mw = required_solar_mwh_yr / (8760 * solar_capacity_factor)
        
        # 3. Size the BESS using the deterministic engineering engine
        bess_power_mw = required_solar_mw * 0.5
        bess_engine = BessSizingEngine()
        bess_res = bess_engine.calculate(
            load_mw=bess_power_mw, 
            duration_hours=4.0, 
            dod_percentage=90.0,
            rte_percentage=90.0
        )
        required_bess_mwh = (bess_power_mw * 4.0) / 0.9
        
        # 4. Calculate CAPEX
        total_solar_capex = required_solar_mw * solar_capex_per_mw
        total_bess_capex = required_bess_mwh * bess_capex_per_mwh
        total_capex = total_solar_capex + total_bess_capex
        
        # 5. Financial Mutual Operation: Carbon Tax Savings
        tax_engine = CarbonTaxLiabilityEngine()
        current_tax_liability = tax_engine.calculate(
            scope1_emissions_tons=0,
            scope2_emissions_tons=current_annual_emissions_tco2e, 
            carbon_tax_rate_usd_per_ton=carbon_tax_rate_per_ton
        )
        future_tax_liability = tax_engine.calculate(
            scope1_emissions_tons=0,
            scope2_emissions_tons=(current_annual_emissions_tco2e - emissions_to_reduce),
            carbon_tax_rate_usd_per_ton=carbon_tax_rate_per_ton
        )
        
        annual_tax_savings = (current_annual_emissions_tco2e * carbon_tax_rate_per_ton) - ((current_annual_emissions_tco2e - emissions_to_reduce) * carbon_tax_rate_per_ton)
        
        # 6. ROI Calculation
        if annual_tax_savings > 0:
            payback_years = total_capex / annual_tax_savings
        else:
            payback_years = float('inf')
            
        result_text = (
            f"**Decarbonization ROI Mutual Operations Analysis:**\n\n"
            f"To achieve a {target_reduction_percentage}% emission reduction ({emissions_to_reduce:.0f} tCO2e/yr), "
            f"the facility requires:\n"
            f"- **Solar PV Installation:** {required_solar_mw:.2f} MW\n"
            f"- **BESS Infrastructure:** {bess_power_mw:.2f} MW / {required_bess_mwh:.2f} MWh\n\n"
            f"**Financial Impact:**\n"
            f"- **Total CAPEX:** ${total_capex:,.2f}\n"
            f"- **Annual Carbon Tax Savings:** ${annual_tax_savings:,.2f} per year\n"
            f"- **ROI / Breakeven Period:** **{payback_years:.1f} Years**\n"
        )
        
        chart_data = {
            "type": "bar",
            "data": {
                "labels": ["Total CAPEX ($)", "10-Year Tax Savings ($)"],
                "datasets": [{
                    "label": "Decarbonization Economics",
                    "data": [total_capex, annual_tax_savings * 10]
                }]
            }
        }
        
        return {
            "result_text": result_text,
            "chart_data": chart_data
        }

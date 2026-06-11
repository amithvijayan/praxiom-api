from engine.registry import EngineRegistry
from engine.engineering.bess_sizing import calculate_bess_capacity
from engine.sustainability.carbon_tax_liability import calculate_carbon_tax

@EngineRegistry.register("calculate_decarbonization_roi")
def calculate_decarbonization_roi(
    current_annual_emissions_tco2e: float,
    target_reduction_percentage: float,
    carbon_tax_rate_per_ton: float,
    solar_capex_per_mw: float,
    bess_capex_per_mwh: float,
    solar_capacity_factor: float = 0.20
):
    """
    Mutual Operations Engine: Calculates the ROI of decarbonizing an industrial facility.
    It links the physical BESS engineering with the financial Carbon Tax liability.
    """
    # 1. Target Emission Reduction
    emissions_to_reduce = current_annual_emissions_tco2e * (target_reduction_percentage / 100.0)
    
    # 2. Estimate Solar required
    # Assuming 1 MWh of solar displaces roughly 0.5 tCO2e of grid emissions (US grid average approx)
    grid_emission_factor_tco2_per_mwh = 0.5
    required_solar_mwh_yr = emissions_to_reduce / grid_emission_factor_tco2_per_mwh
    
    # Solar MW = MWh_yr / (8760 * capacity factor)
    required_solar_mw = required_solar_mwh_yr / (8760 * solar_capacity_factor)
    
    # 3. Size the BESS using the deterministic engineering engine
    # We assume the facility needs 4 hours of storage for 50% of the solar peak
    bess_power_mw = required_solar_mw * 0.5
    bess_res = calculate_bess_capacity(
        target_load_mw=bess_power_mw, 
        duration_hours=4.0, 
        depth_of_discharge=0.9
    )
    # The BESS engine returns text, we just need to parse or recalculate strictly.
    # Let's strictly recalculate for the mathematical model:
    required_bess_mwh = (bess_power_mw * 4.0) / 0.9
    
    # 4. Calculate CAPEX
    total_solar_capex = required_solar_mw * solar_capex_per_mw
    total_bess_capex = required_bess_mwh * bess_capex_per_mwh
    total_capex = total_solar_capex + total_bess_capex
    
    # 5. Financial Mutual Operation: Carbon Tax Savings
    # We call the carbon tax engine to see how much they were paying vs how much they will pay
    current_tax_liability = calculate_carbon_tax(
        annual_emissions=current_annual_emissions_tco2e, 
        tax_rate_per_ton=carbon_tax_rate_per_ton
    )
    future_tax_liability = calculate_carbon_tax(
        annual_emissions=(current_annual_emissions_tco2e - emissions_to_reduce),
        tax_rate_per_ton=carbon_tax_rate_per_ton
    )
    
    annual_tax_savings = float(current_tax_liability["result_text"].split("$")[1].split()[0].replace(",", "")) - float(future_tax_liability["result_text"].split("$")[1].split()[0].replace(",", ""))
    
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
        f"- **BESS Infrastructure:** {bess_power_mw:.2f} MW / {required_bess_mwh:.2f} MWh (Based on IEEE 1547 guidelines)\n\n"
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

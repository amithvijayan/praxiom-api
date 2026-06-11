from engine.engineering.nuclear_smr import NuclearSMREngine
from engine.sustainability.green_hydrogen import GreenHydrogenViabilityEngine
from engine.sustainability.lifecycle_carbon import LifecycleCarbonAssessmentEngine
from engine.utility_business.ppa_modeler import PowerPurchaseAgreementEngine

class OmniSystemMasterplanEngine:
    def calculate(self, smr_thermal_mw: float, ppa_strike_price: float) -> dict:
        """
        The ultimate Mutual Operations engine.
        Simultaneously models a Nuclear SMR, diverts 50% power to Green Hydrogen,
        offsets its lifecycle carbon, and models the PPA revenue for the remaining 50% grid export.
        """
        try:
            # 1. Nuclear SMR Output (Assume 33% thermal efficiency)
            smr_engine = NuclearSMREngine()
            smr_res = smr_engine.calculate(smr_thermal_mw, 0.33)
            if smr_res['status'] == 'error': return smr_res
            mwe_total = smr_res['chart_data']['data']['datasets'][0]['data'][1]
            
            # 2. Green Hydrogen (Divert 50% of MWe)
            h2_engine = GreenHydrogenViabilityEngine()
            h2_res = h2_engine.calculate(mwe_total * 0.5, ppa_strike_price)
            h2_tons = h2_res['chart_data']['data']['datasets'][0]['data'][1]
            
            # 3. PPA Revenue for Grid Export (Remaining 50% MWe)
            ppa_engine = PowerPurchaseAgreementEngine()
            annual_export_mwh = (mwe_total * 0.5) * 8760 * 0.95
            ppa_res = ppa_engine.calculate(annual_export_mwh, ppa_strike_price, term_years=20)
            
            # 4. Lifecycle Carbon (Assume 200,000 kg steel/concrete for the SMR)
            lca_engine = LifecycleCarbonAssessmentEngine()
            lca_res = lca_engine.calculate(200_000, 500, 40, energy_per_year_kwh=0, grid_carbon_intensity_kg_kwh=0)
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Total Output (MWe)", "H2 Allocation (MWe)", "Grid Export (MWe)"],
                    "datasets": [{
                        "label": "OmniSystem Power Architecture",
                        "data": [round(mwe_total), round(mwe_total*0.5), round(mwe_total*0.5)]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": (
                    f"> **[PASS] OMNISYSTEM MASTERPLAN: NUCLEAR-H2 HYBRID**\n"
                    f"Initiated comprehensive mutual operations for a {smr_thermal_mw} MWth Nuclear SMR.\n\n"
                    f"- **Electrical Capacity**: {round(mwe_total)} MWe Gross\n"
                    f"- **Green Hydrogen**: 50% power diverted to electrolyzers. Yields {round(h2_tons)} tons H2/year.\n"
                    f"- **Grid Export PPA**: Remaining 50% sold at ${ppa_strike_price}/MWh. "
                    f"20-Yr Revenue: ${round(ppa_res['chart_data']['data']['datasets'][0]['data'][19]/1_000_000, 2)} Million.\n"
                    f"- **Lifecycle Carbon**: SMR Embodied Carbon totals {round(lca_res['chart_data']['data']['datasets'][0]['data'][2], 1)} tCO2e. Zero operational emissions."
                ),
                "chart_data": chart_data
            }
        except Exception as e:
            return {"status": "error", "result": f"OmniSystem masterplan failed: {str(e)}"}

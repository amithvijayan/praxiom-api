from engine.registry import EngineRegistry
import math

@EngineRegistry.register("transformer_sizing")
class TransformerSizingEngine:
    """
    Calculates required Transformer Nameplate Capacity (kVA) and full load currents 
    based on peak load (kW), power factor, primary/secondary voltages.
    """
    
    def calculate(
        self,
        peak_load_kw: float,
        power_factor: float = 0.85,
        primary_voltage_kv: float = 13.8,
        secondary_voltage_kv: float = 0.48,
        safety_margin_percentage: float = 25.0
    ):
        # 1. Calculate Required kVA (Load / Power Factor)
        base_kva = peak_load_kw / power_factor
        
        # 2. Apply Safety Margin for continuous load / future growth
        required_kva = base_kva * (1 + (safety_margin_percentage / 100))
        
        # 3. Round up to nearest standard size (e.g., 500, 750, 1000, 1500, 2000 kVA)
        standard_sizes = [75, 112.5, 150, 225, 300, 500, 750, 1000, 1500, 2000, 2500, 3750, 5000, 7500, 10000]
        selected_kva = next((size for size in standard_sizes if size >= required_kva), required_kva)
        
        # 4. Calculate Full Load Currents (3-phase)
        # I = kVA / (sqrt(3) * kV)
        sqrt_3 = math.sqrt(3)
        primary_current_amps = selected_kva / (sqrt_3 * primary_voltage_kv)
        secondary_current_amps = selected_kva / (sqrt_3 * secondary_voltage_kv)
        
        result_text = (
            f"Transformer Physics Output: To support a peak load of {peak_load_kw} kW "
            f"at a power factor of {power_factor}, a minimum of {round(required_kva, 2)} kVA is needed. "
            f"With a {safety_margin_percentage}% margin, the recommended standard Nameplate Capacity is {selected_kva} kVA. "
            f"Full Load Currents: {round(primary_current_amps, 2)} A (Primary {primary_voltage_kv}kV) / {round(secondary_current_amps, 2)} A (Secondary {secondary_voltage_kv}kV)."
        )
        
        chart_data = [
            {"name": "Peak Load (kVA)", "value": round(base_kva, 2)},
            {"name": "Safety Margin (kVA)", "value": round(required_kva - base_kva, 2)},
            {"name": "Selected Standard (kVA)", "value": selected_kva}
        ]
        
        return {
            "result_text": result_text,
            "chart_data": chart_data
        }

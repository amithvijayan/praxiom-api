from engine.registry import EngineRegistry
import math

@EngineRegistry.register("calculate_load_flow")
def calculate_load_flow(
    sending_voltage_kv: float,
    load_mw: float,
    power_factor: float,
    line_length_km: float,
    resistance_per_km: float = 0.1,
    reactance_per_km: float = 0.4
):
    """
    Perform a deterministic load flow analysis and short-circuit fault current estimation.
    """
    # 1. Calculate Line Parameters
    R = resistance_per_km * line_length_km
    X = reactance_per_km * line_length_km
    Z = math.sqrt(R**2 + X**2)
    
    # 2. Calculate Current
    # P = sqrt(3) * V * I * pf  => I = P / (sqrt(3) * V * pf)
    current_amps = (load_mw * 1000) / (math.sqrt(3) * sending_voltage_kv * power_factor)
    
    # 3. Calculate Voltage Drop Approximation
    # VD = sqrt(3) * I * (R*cos(phi) + X*sin(phi))
    phi = math.acos(power_factor)
    voltage_drop_v = math.sqrt(3) * current_amps * (R * power_factor + X * math.sin(phi))
    voltage_drop_kv = voltage_drop_v / 1000
    
    receiving_voltage_kv = sending_voltage_kv - voltage_drop_kv
    voltage_drop_percentage = (voltage_drop_kv / sending_voltage_kv) * 100
    
    # 4. Short-Circuit Fault Estimation (at the receiving end bus)
    # Assuming infinite source bus for absolute worst-case short circuit
    # I_sc = V_phase / Z
    fault_current_ka = (sending_voltage_kv / math.sqrt(3)) / Z
    
    # 5. Output Formatting
    result_text = (
        f"**Load Flow & Grid Integration Physics Analysis:**\n\n"
        f"- **Transmission Line Impedance:** R={R:.3f} Ω, X={X:.3f} Ω, Z={Z:.3f} Ω\n"
        f"- **Load Current:** {current_amps:.2f} A\n"
        f"- **Voltage Drop:** {voltage_drop_kv:.2f} kV ({voltage_drop_percentage:.2f}%)\n"
        f"- **Receiving End Voltage:** {receiving_voltage_kv:.2f} kV\n\n"
        f"**Short Circuit Analysis:**\n"
        f"- Estimated 3-Phase Fault Current at receiving bus: **{fault_current_ka:.2f} kA**\n\n"
    )
    
    if voltage_drop_percentage > 5.0:
        result_text += "> **[WARNING] Grid Instability Detected:** Voltage drop exceeds the standard 5% limit. Reactive power compensation (e.g., STATCOM or capacitor banks) is strictly required.\n"
    else:
        result_text += "> **[PASS] Grid Stability:** Voltage drop is within the acceptable 5% limits. No major reactive power compensation required.\n"
        
    chart_data = {
        "type": "bar",
        "data": {
            "labels": ["Sending Voltage (kV)", "Receiving Voltage (kV)"],
            "datasets": [{
                "label": "Bus Voltage Profile",
                "data": [sending_voltage_kv, receiving_voltage_kv]
            }]
        }
    }
    
    return {
        "result_text": result_text,
        "chart_data": chart_data
    }

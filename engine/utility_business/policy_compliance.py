from engine.registry import EngineRegistry

@EngineRegistry.register("check_policy_compliance")
def check_policy_compliance(
    region: str,
    project_type: str,
    capacity_mw: float
):
    """
    Deterministic rules engine to cross-reference physical engineering projects 
    with specific regional regulations and standards.
    """
    region = region.upper()
    project_type = project_type.upper()
    
    warnings = []
    requirements = []
    
    # Example Rules Database Matrix
    if region in ["EU", "EUROPE"]:
        requirements.append("Compliance with EU Green Deal taxonomy required.")
        if project_type == "BESS":
            requirements.append("Must meet EU Battery Regulation (2023/1542) for carbon footprint and recycling.")
        if capacity_mw > 50:
            warnings.append("Projects > 50 MW require an extensive Environmental Impact Assessment (EIA) under EU Directives.")
            
    elif region in ["US", "USA", "NORTH AMERICA"]:
        if project_type in ["BESS", "SOLAR", "MICROGRID"]:
            requirements.append("Must comply with IEEE 1547-2018 for interconnecting distributed resources with electric power systems.")
            requirements.append("FERC Order 2222 applies: Project can participate in regional wholesale markets.")
        if capacity_mw > 20:
            warnings.append("Projects > 20 MW fall under Large Generator Interconnection Procedures (LGIP). Expect 12-24 month interconnection queue delays.")
            
    else:
        requirements.append("Standard IEC grid compliance required.")
        warnings.append("Please verify local interconnection rules with the regional Transmission System Operator (TSO).")
        
    result_text = f"**Regulatory & Policy Compliance Report**\n\n"
    result_text += f"- **Region:** {region}\n"
    result_text += f"- **Project Type:** {project_type} ({capacity_mw} MW)\n\n"
    
    if requirements:
        result_text += "**Mandatory Requirements:**\n"
        for req in requirements:
            result_text += f"- {req}\n"
        result_text += "\n"
        
    if warnings:
        result_text += "> **[WARNING] Critical Compliance Flags:**\n"
        for warn in warnings:
            result_text += f"> - {warn}\n"
            
    return {
        "result_text": result_text,
        "chart_data": None
    }

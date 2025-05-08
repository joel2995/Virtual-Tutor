# backend/stitching_api.py

def generate_stitching_process(measurements, prompt):
    """
    Generate a detailed stitching process based on body measurements and user style prompt.
    """
    # Extract measurements
    height = measurements.get("height_cm", "unknown")
    shoulder = measurements.get("shoulder_width_cm", "unknown")
    bust = measurements.get("bust_cm", "unknown")
    waist = measurements.get("waist_cm", "unknown")
    hip = measurements.get("hip_cm", "unknown")
    arm_length = measurements.get("arm_length_cm", "unknown")
    inseam = measurements.get("inseam_cm", "unknown")
    
    # Analyze prompt for clothing type
    prompt_lower = prompt.lower()
    
    # Determine clothing type from prompt
    if any(word in prompt_lower for word in ["dress", "gown"]):
        clothing_type = "dress"
    elif any(word in prompt_lower for word in ["shirt", "blouse", "top"]):
        clothing_type = "top"
    elif any(word in prompt_lower for word in ["pants", "trousers", "jeans"]):
        clothing_type = "pants"
    elif any(word in prompt_lower for word in ["skirt"]):
        clothing_type = "skirt"
    else:
        clothing_type = "general"
    
    # Generate fabric requirements
    fabric_requirements = generate_fabric_requirements(clothing_type, measurements)
    
    # Generate custom measurements
    custom_measurements = generate_custom_measurements(clothing_type, measurements)
    
    # Generate stitching steps
    stitching_steps = generate_stitching_steps(clothing_type, prompt)
    
    # Generate additional notes
    notes = generate_notes(clothing_type, prompt)
    
    return {
        "fabric_requirements": fabric_requirements,
        "custom_measurements": custom_measurements,
        "stitching_steps": stitching_steps,
        "notes": notes
    }

def generate_fabric_requirements(clothing_type, measurements):
    """Generate fabric requirements based on clothing type and measurements"""
    height = measurements.get("height_cm", 170)
    bust = measurements.get("bust_cm", 90)
    hip = measurements.get("hip_cm", 100)
    
    if clothing_type == "dress":
        fabric_length = height * 1.5 / 100  # Convert to meters
        return f"{fabric_length:.1f} meters of fabric (width 150cm)"
    elif clothing_type == "top":
        fabric_length = height * 0.7 / 100
        return f"{fabric_length:.1f} meters of fabric (width 150cm)"
    elif clothing_type == "pants":
        fabric_length = height * 1.2 / 100
        return f"{fabric_length:.1f} meters of fabric (width 150cm)"
    elif clothing_type == "skirt":
        fabric_length = height * 0.6 / 100
        return f"{fabric_length:.1f} meters of fabric (width 150cm)"
    else:
        fabric_length = height * 1.0 / 100
        return f"{fabric_length:.1f} meters of fabric (width 150cm)"

def generate_custom_measurements(clothing_type, measurements):
    """Generate custom measurements based on clothing type"""
    custom_measurements = []
    
    if clothing_type == "dress" or clothing_type == "top":
        bust = measurements.get("bust_cm", "unknown")
        waist = measurements.get("waist_cm", "unknown")
        shoulder = measurements.get("shoulder_width_cm", "unknown")
        arm_length = measurements.get("arm_length_cm", "unknown")
        
        custom_measurements.append(f"Bust: {bust} cm (add 4-6 cm ease)")
        custom_measurements.append(f"Waist: {waist} cm (add 2-4 cm ease)")
        custom_measurements.append(f"Shoulder width: {shoulder} cm")
        custom_measurements.append(f"Sleeve length: {arm_length} cm")
        
    if clothing_type == "dress" or clothing_type == "skirt" or clothing_type == "pants":
        hip = measurements.get("hip_cm", "unknown")
        waist = measurements.get("waist_cm", "unknown")
        inseam = measurements.get("inseam_cm", "unknown")
        
        custom_measurements.append(f"Hip: {hip} cm (add 4-6 cm ease)")
        custom_measurements.append(f"Waist: {waist} cm (add 2-4 cm ease)")
        
        if clothing_type == "pants":
            custom_measurements.append(f"Inseam: {inseam} cm")
    
    return custom_measurements

def generate_stitching_steps(clothing_type, prompt):
    """Generate stitching steps based on clothing type and prompt"""
    
    common_steps = [
        "Prepare your fabric by washing, drying, and ironing it.",
        "Lay out and cut your pattern pieces according to the measurements.",
        "Mark all darts, pleats, and other details on the wrong side of the fabric."
    ]
    
    if clothing_type == "dress":
        specific_steps = [
            "Sew darts on bodice front and back pieces.",
            "Join shoulder seams.",
            "Attach sleeves to armholes (if applicable).",
            "Sew side seams of bodice and skirt separately.",
            "Join bodice to skirt at waistline.",
            "Insert zipper or other closure.",
            "Finish neckline with facing or binding.",
            "Hem sleeves and bottom edge."
        ]
    elif clothing_type == "top":
        specific_steps = [
            "Sew darts on front and back pieces.",
            "Join shoulder seams.",
            "Attach sleeves to armholes (if applicable).",
            "Sew side seams.",
            "Finish neckline with facing or binding.",
            "Hem sleeves and bottom edge."
        ]
    elif clothing_type == "pants":
        specific_steps = [
            "Sew front darts or pleats.",
            "Join front and back at inseam.",
            "Join front and back at outseam.",
            "Create casing for elastic or attach waistband.",
            "Insert zipper or other closure.",
            "Hem bottom edges."
        ]
    elif clothing_type == "skirt":
        specific_steps = [
            "Sew darts or pleats.",
            "Join side seams.",
            "Create casing for elastic or attach waistband.",
            "Insert zipper or other closure.",
            "Hem bottom edge."
        ]
    else:
        specific_steps = [
            "Join main seams according to pattern.",
            "Attach any additional pieces.",
            "Finish edges appropriately.",
            "Add closures as needed.",
            "Hem all raw edges."
        ]
    
    # Add customization based on prompt
    if "pleated" in prompt.lower():
        specific_steps.insert(1, "Create pleats according to pattern markings.")
    if "gathered" in prompt.lower():
        specific_steps.insert(1, "Run gathering stitches and gather fabric as marked.")
    if "collar" in prompt.lower():
        specific_steps.insert(-2, "Prepare and attach collar according to pattern.")
    if "pocket" in prompt.lower():
        specific_steps.insert(-2, "Prepare and attach pockets as desired.")
        
    return common_steps + specific_steps

def generate_notes(clothing_type, prompt):
    """Generate additional notes based on clothing type and prompt"""
    
    notes = "For best results, make a test garment (muslin) first to check the fit."
    
    # Add fabric suggestions based on prompt
    if "summer" in prompt.lower():
        notes += " Consider using lightweight fabrics like cotton, linen, or rayon for better breathability."
    elif "winter" in prompt.lower():
        notes += " Consider using warmer fabrics like wool, flannel, or thick cotton for better insulation."
    elif "formal" in prompt.lower() or "elegant" in prompt.lower():
        notes += " Consider using silk, satin, or fine wool for a more elegant appearance."
    
    # Add construction tips
    if clothing_type == "dress" or clothing_type == "top":
        notes += " Pay special attention to the fit around the bust and shoulders."
    if clothing_type == "pants":
        notes += " Ensure proper fit at the waist and hips for comfort."
    
    return notes

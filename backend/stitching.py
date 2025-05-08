def generate_stitching_instructions(measurements, prompt):
    """
    Generate stitching instructions based on measurements and prompt.
    
    Args:
        measurements: Dictionary containing body measurements
        prompt: User's description of the desired dress
        
    Returns:
        Dictionary containing stitching instructions
    """
    # In a real application, you might use an AI model like GPT-4 here
    # For this example, we'll use a rule-based approach
    
    # Extract keywords from the prompt
    prompt_lower = prompt.lower()
    
    # Determine dress type
    dress_type = "regular"
    if "wedding" in prompt_lower or "bridal" in prompt_lower:
        dress_type = "wedding"
    elif "evening" in prompt_lower or "gown" in prompt_lower:
        dress_type = "evening"
    elif "summer" in prompt_lower or "casual" in prompt_lower:
        dress_type = "summer"
    elif "formal" in prompt_lower:
        dress_type = "formal"
    
    # Determine fabric type
    fabric = "cotton"
    if "silk" in prompt_lower:
        fabric = "silk"
    elif "chiffon" in prompt_lower:
        fabric = "chiffon"
    elif "linen" in prompt_lower:
        fabric = "linen"
    elif "satin" in prompt_lower:
        fabric = "satin"
    
    # Determine length
    length = "knee-length"
    if "maxi" in prompt_lower or "long" in prompt_lower:
        length = "maxi"
    elif "mini" in prompt_lower or "short" in prompt_lower:
        length = "mini"
    
    # Determine sleeve type
    sleeve = "short"
    if "sleeveless" in prompt_lower:
        sleeve = "sleeveless"
    elif "long sleeve" in prompt_lower:
        sleeve = "long"
    elif "three-quarter" in prompt_lower or "3/4" in prompt_lower:
        sleeve = "three-quarter"
    
    # Calculate fabric requirements
    fabric_amount = 0
    if length == "mini":
        fabric_amount = 1.5
    elif length == "knee-length":
        fabric_amount = 2.5
    else:  # maxi
        fabric_amount = 3.5
    
    if sleeve == "long":
        fabric_amount += 0.5
    
    # Adjust for body size
    if measurements['bust'] > 100 or measurements['hips'] > 110:
        fabric_amount += 0.5
    
    # Generate custom measurements
    custom_measurements = [
        f"Bust: {measurements['bust']} cm + 4 cm ease = {measurements['bust'] + 4} cm",
        f"Waist: {measurements['waist']} cm + 2 cm ease = {measurements['waist'] + 2} cm",
        f"Hips: {measurements['hips']} cm + 6 cm ease = {measurements['hips'] + 6} cm",
        f"Shoulder width: {measurements['shoulder_width']} cm",
        f"Sleeve length: {measurements['arm_length']} cm (adjust for {sleeve} sleeves)"
    ]
    
    # Generate stitching steps based on dress type
    steps = []
    
    # Common steps for all dress types
    steps.append("Take body measurements and add ease allowances")
    steps.append(f"Purchase {fabric_amount} meters of {fabric} fabric")
    steps.append("Wash and iron the fabric before cutting")
    steps.append("Cut the fabric according to the pattern pieces")
    
    # Specific steps based on dress type
    if dress_type == "wedding":
        steps.append("Cut lining fabric for bodice and skirt")
        steps.append("Sew darts on bodice front and back pieces")
        steps.append("Attach bodice front and back at shoulders")
        steps.append("Sew side seams of bodice")
        steps.append("Repeat for lining")
        steps.append("Attach bodice to lining at neckline and armholes")
        steps.append("Sew skirt panels together")
        steps.append("Gather skirt at waistline")
        steps.append("Attach skirt to bodice")
        steps.append("Insert zipper at back")
        steps.append("Hem the skirt")
        steps.append("Add embellishments as desired")
    elif dress_type == "evening":
        steps.append("Sew darts on bodice front and back pieces")
        steps.append("Attach bodice front and back at shoulders")
        steps.append("Sew side seams of bodice")
        steps.append("Finish neckline with facing or bias binding")
        steps.append("Sew skirt panels together")
        steps.append("Attach skirt to bodice")
        steps.append("Insert zipper at back or side")
        steps.append("Hem the skirt")
    else:  # casual, summer, regular
        steps.append("Sew shoulder seams")
        steps.append("Attach sleeves if applicable")
        steps.append("Sew side seams from sleeve edge to hem")
        steps.append("Finish neckline with facing or bias binding")
        steps.append("Hem sleeves and bottom edge")
    
    # Additional notes
    notes = f"This {dress_type} dress in {fabric} fabric is designed to be {length} with {sleeve} sleeves. "
    
    if fabric == "silk" or fabric == "satin":
        notes += "Use a fine needle and pins to avoid damaging the fabric. "
    
    if dress_type == "wedding" or dress_type == "evening":
        notes += "Consider adding a lining for better structure and comfort. "
    
    if "pattern" in prompt_lower or "print" in prompt_lower:
        notes += "When cutting patterned fabric, ensure the pattern aligns at seams. "
    
    # Return the stitching information
    return {
        "fabricRequirements": f"{fabric_amount} meters of {fabric} fabric",
        "customMeasurements": custom_measurements,
        "steps": steps,
        "notes": notes
    }
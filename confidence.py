def calculate_confidence(input_text, output_text):
    if len(output_text) == 0:
        return "Low"
    elif len(output_text) > len(input_text) / 2:
        return "High"
    else:
        return "Medium"

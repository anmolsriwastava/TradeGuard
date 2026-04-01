def generate_response(risk):
    
    if risk > 80:
        return "Transship via alternate route"
    
    elif risk > 60:
        return "Notify buyer"
    
    else:
        return "Proceed normally"
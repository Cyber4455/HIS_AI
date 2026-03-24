from datetime import datetime

def format_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        return date_str

def get_risk_color(risk_level: str) -> str:
    colors = {
        "Low": "green",
        "Medium": "yellow", 
        "High": "red",
        "Critical": "darkred"
    }
    return colors.get(risk_level, "gray")

def get_risk_emoji(risk_level: str) -> str:
    emojis = {
        "Low": "🟢",
        "Medium": "🟡",
        "High": "🔴",
        "Critical": "⚠️"
    }
    return emojis.get(risk_level, "⚪")

def validate_age(age: int) -> bool:
    return 1 <= age <= 120

def validate_bmi(bmi: float) -> bool:
    return 10 <= bmi <= 60

def validate_blood_pressure(sys: int, dia: int) -> bool:
    return (60 <= sys <= 250) and (40 <= dia <= 150)

def validate_heart_rate(hr: int) -> bool:
    return 30 <= hr <= 220

def validate_glucose(glucose: float) -> bool:
    return 30 <= glucose <= 600

def categorize_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def categorize_blood_pressure(sys: int, dia: int) -> str:
    if sys < 120 and dia < 80:
        return "Normal"
    elif sys < 130 and dia < 80:
        return "Elevated"
    elif sys < 140 or dia < 90:
        return "High (Stage 1)"
    else:
        return "High (Stage 2)"

def categorize_glucose(glucose: float) -> str:
    if glucose < 100:
        return "Normal"
    elif glucose < 126:
        return "Prediabetes"
    else:
        return "Diabetes"

def categorize_cholesterol(chol: int) -> str:
    if chol < 200:
        return "Desirable"
    elif chol < 240:
        return "Borderline High"
    else:
        return "High"

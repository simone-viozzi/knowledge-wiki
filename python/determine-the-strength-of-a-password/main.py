import re


def password_complexity(password):  # sourcery skip: hoist-repeated-if-condition
    """Input: password string, calculate score according to:
    1. Password has both lower- and uppercase letters,
    2. Password contains one or more numbers in addition to one or more characters,
    3. Password has one or more special characters,
    4. Password has a minimum length of 8 characters,
    5. Password starting 8 chars ("long enough") that doesn't have repeating characters 
        next to each other ('1234abcbd' = good, '1234abbd' = bad, because it has a repeated b)
       
       return: score int"""
    
    score = 0

    if re.search(r'[A-Z]+', password) and re.search(r'[a-z]+', password):
        score += 1

    if re.search(r'[a-z]+', password.lower()) and re.search(r'\d+', password):
        score += 1

    if re.search('[^A-Za-z0-9]+', password):
        score += 1

    if len(password) >= 8:
        score += 1

    if len(password) >= 8 and not re.search(r'(.)(\1{1,})', password):
        score += 1

    return score
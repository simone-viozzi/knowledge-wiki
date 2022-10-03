import re


def password_complexity(password):
    """Input: password string, calculate score according to:
    1. Password has both lower- and uppercase letters,
    2. Password contains one or more numbers in addition to one or more characters,
    3. Password has one or more special characters,
    4. Password has a minimum length of 8 characters,
    5. Password starting 8 chars ("long enough") that doesn't have repeating characters 
        next to each other ('1234abcbd' = good, '1234abbd' = bad, because it has a repeated b)
       
       return: score int"""
    
    print(password)
    score = 0
    if re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        print('1')
        score += 1
    if re.search(r'[0-9]', password) and re.search(r'[a-zA-Z]', password):
        print('2')
        score += 1
    if re.search(r'[^a-zA-Z0-9]', password):
        print('3')
        score += 1
    if len(password) >= 8:
        print('4')
        score += 1
    if len(password) >= 8 and not re.search(r'(.)\1', password):
        print('5')
        score += 1
    return score
# Determine the strength of a password

In this Bite you evaluate the strength of a password. Complete the function below and return a score from 0 to 5. Each of the following matches increases the score by one:

1. Password has both lower- and uppercase letters,
1. Password contains one or more numbers in addition to one or more characters,
1. Password has one or more special characters,
1. Password has a minimum length of 8 characters,
1. Password starting 8 chars ("long enough") that doesn't have repeating characters ('1234abcbd' = good, '1234abbd' = bad, because it has a repeated b)

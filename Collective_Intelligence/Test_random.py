def gcd(a, b):
    """ Euclid Theorom or Algorithm
        the GCD of Two numbers
            is smallest number + reminder of the greatest/smallest number
            if greatest number is not divisible by smallest number
        in case greatest number divisble then smallest number is the GCD
    """
    print ("Somebody calling gcd")
    while b:
        print (a, b, a%b)
        a, b = b, a % b
    print ("Returning gcd")
    return a

print (gcd(126, 85))
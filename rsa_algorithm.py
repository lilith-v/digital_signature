import random
#from db_utils import db_connection


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    if temp_phi == 1:
        return d + phi

def generate_key_pair(p, q):
        if p == q:
             raise ValueError('p and q cannot be equal')
        n = p * q
        # Phi is the totient of n
        phi = (p-1) * (q-1)
        # 1 < e < phi
        e = random.randrange(1, phi)
        # Use Euclid's Algorithm to verify that e and phi(n) are coprime
        g = gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = gcd(e, phi)
        # Use Extended Euclid's Algorithm to generate the private key
        d = multiplicative_inverse(e, phi)
        # Public key is (e, n) and private key is (d, n)
        print('e = ', e)
        print('d = ', d)
        print('n = ', n)
        return ((e, n), (d, n))




def encrypt(public_key, msg):
    if not isinstance(public_key, tuple) or len(public_key) != 2:
        raise ValueError("Invalid public key")
    key, n = public_key
    cypher = ""
    for c in msg:
        m = ord(c)
        cypher += str(pow(m, key, n)) 
        cypher += "\n"
    print('cypher = ', cypher)
    return cypher



def decrypt(private_key, cyphertext):
    if not isinstance(private_key, tuple) or len(private_key) != 2:
        raise ValueError("Invalid private key")

    key, n = private_key
    msg = ""
    parts = cyphertext.split()
    for part in parts:
        if part:
            c = int(part)
            msg += chr(pow(c, key, n))

    return msg


import math

def rotr(num, shift, bits=64):
    num &= (2 ** bits - 1)
    return (num >> shift) | ((num & (2 ** shift - 1)) << (bits - shift))

def BSIG0(word):
    return rotr(word, 28) ^ rotr(word, 34) ^ rotr(word, 39)

def BSIG1(word):
    return rotr(word, 14) ^ rotr(word, 18) ^ rotr(word, 41)

def choice(e, f, g):
    return (e & f) ^ ((~e) & g)

def majority(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)

def SSIG0(word):
    return rotr(word, 1) ^ rotr(word, 8) ^ (word >> 7)


def SSIG1(word):
    return rotr(word, 19) ^ rotr(word, 61) ^ (word >> 6)


def ascii_to_binary(text):
    # Convert input message into a binary sequence
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    original_length = len(binary_string)

    # Append the '1' bit
    binary_string += '1'

    # Calculate the padding needed to make the total length 896 mod 1024
    padding_needed = (896 - (len(binary_string) % 1024)) % 1024
    binary_string += '0' * padding_needed

    # Append the original length as a 128-bit binary number
    binary_string += format(original_length, '0128b')

    # Ensure the total length is a multiple of 1024
    if len(binary_string) % 1024 != 0:
        raise ValueError(f"Binary message length after padding must be a multiple of 1024 bits. Current length: {len(binary_string)} bits.")

    return binary_string


def hash_values():
    # Generate round constants from square roots of the first 8 primes
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    hex_values = {}
    for prime in primes:
        sqrt_p = math.sqrt(prime)
        fractional_part = sqrt_p % 1
        scaled_fraction = int(fractional_part * (1 << 64))
        hex_value = scaled_fraction.to_bytes(8, 'big').hex()
        hex_values[prime] = hex_value
    return hex_values


hash_value = hash_values()


def round_constants():
    # Generate round constants from cube roots of the first 80 primes
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
        227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
        307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383,
        389, 397, 401, 409
    ]
    constants = {}
    for prime in primes:
        cbrt_p = prime ** (1.0 / 3)
        fractional_part = cbrt_p % 1
        scaled_fraction = int(fractional_part * (1 << 64))
        hex_val = scaled_fraction.to_bytes(8, 'big').hex()
        constants[prime] = hex_val
    return constants


constants = round_constants()


def word_values(binary_message):
    # Split into 64-bit chunks and convert to integers
    words = [int(binary_message[i:i + 64], 2) for i in range(0, 1024, 64)]

    # Extend to 80 words
    for i in range(16, 80):
        words.append((SSIG1(words[i - 2]) + words[i - 7] + SSIG0(words[i - 15]) + words[i - 16]) & 0xFFFFFFFFFFFFFFFF)

    return words


def compression_round(a, b, c, d, e, f, g, h, k, w):
    T1 = (h + BSIG1(e) + choice(e, f, g) + int(k, 16) + w) & 0xFFFFFFFFFFFFFFFF
    T2 = (BSIG0(a) + majority(a, b, c)) & 0xFFFFFFFFFFFFFFFF
    h = g
    g = f
    f = e
    e = (d + T1) & 0xFFFFFFFFFFFFFFFF
    d = c
    c = b
    b = a
    a = (T1 + T2) & 0xFFFFFFFFFFFFFFFF
    return a, b, c, d, e, f, g, h


def full_compression_process(binary_message):
    words = word_values(binary_message)
    constants_list = list(constants.values())

    # Initial hash values
    a, b, c, d = 0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1
    e, f, g, h = 0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179

    for i in range(80):
        a, b, c, d, e, f, g, h = compression_round(
            a, b, c, d, e, f, g, h, constants_list[i], words[i]
        )

    # Add compressed chunk to current hash value
    a = (a + int(hash_value[2], 16)) & 0xFFFFFFFFFFFFFFFF
    b = (b + int(hash_value[3], 16)) & 0xFFFFFFFFFFFFFFFF
    c = (c + int(hash_value[5], 16)) & 0xFFFFFFFFFFFFFFFF
    d = (d + int(hash_value[7], 16)) & 0xFFFFFFFFFFFFFFFF
    e = (e + int(hash_value[11], 16)) & 0xFFFFFFFFFFFFFFFF
    f = (f + int(hash_value[13], 16)) & 0xFFFFFFFFFFFFFFFF
    g = (g + int(hash_value[17], 16)) & 0xFFFFFFFFFFFFFFFF
    h = (h + int(hash_value[19], 16)) & 0xFFFFFFFFFFFFFFFF

    # Concatenate the final hash values
    return f"{a:016x}{b:016x}{c:016x}{d:016x}{e:016x}{f:016x}{g:016x}{h:016x}"


def main():
    while True:
        text = input("Enter text: ")
        binary_message = ascii_to_binary(text)
        final_hash = full_compression_process(binary_message)
        print(f"\nFinal Hash: {final_hash}")

        user_choice = input("Do you want to hash another message? (y/n): ").strip().lower()
        if user_choice != "y":
            print("Exiting!")
            break

main()

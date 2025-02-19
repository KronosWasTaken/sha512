# SHA-512 Hash Implementation in Python

This project is a custom implementation of the **SHA-512 hashing algorithm** in Python. It processes input text, converts it into a binary format, applies padding, generates message schedules, and performs compression rounds to produce a **512-bit hash**.

## Features

- Implements **SHA-512** using bitwise operations.
- Uses **rotation, shifting, and logical operations** as per the SHA-512 standard.
- Generates **initial hash values** and **round constants** dynamically.
- Supports **multiple hashing sessions** in a loop.

## How It Works

### Message Preprocessing
- Converts text input to binary.
- Pads the message to fit the SHA-512 block size.
- Appends the message length.

### Message Schedule
- Expands the 1024-bit block into 80 words using bitwise operations.

### Compression Rounds
- Performs **80 rounds** of hashing using SHA-512 functions.

### Final Hash
- Produces a **512-bit (128-hex character) digest**.

## Functions Breakdown

- **`rotr(num, shift, bits=64)`** - Rotates bits to the right.
- **`BSIG0(word), BSIG1(word)`** - SHA-512 **big sigma** functions.
- **`SSIG0(word), SSIG1(word)`** - SHA-512 **small sigma** functions.
- **`choice(e, f, g)`** - Chooses bits based on `e`.
- **`majority(a, b, c)`** - Computes the majority function.
- **`ascii_to_binary(text)`** - Converts text to **padded binary**.
- **`hash_values()`** - Generates **initial hash values** from square roots of primes.
- **`round_constants()`** - Generates **SHA-512 round constants**.
- **`word_values(binary_message)`** - Expands 1024-bit blocks to 80 words.
- **`compression_round(a, b, c, d, e, f, g, h, k, w)`** - One round of compression.
- **`full_compression_process(binary_message)`** - Processes the **full hash computation**.


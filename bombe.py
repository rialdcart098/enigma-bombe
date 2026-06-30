from enigma import EnigmaMachine, Rotor, Reflector
import random

class Bombe:
    def __init__(self, make_machine, crib, ciphertext):
        self.make_machine = make_machine
        self.crib = crib.upper()
        self.ciphertext = ciphertext.upper()
    def test_setting(self, p1, p2, p3):
        machine = self.make_machine()
        machine.set_positions(p1, p2, p3)
        decrypted = machine.encrypt(self.ciphertext)
        return self.crib in decrypted
    def crack(self):
        matches = []
        total = 26 * 26 * 26
        tested = 0
        for p1 in range(26):
            for p2 in range(26):
                for p3 in range(26):
                    tested += 1
                    if self.test_setting(p1, p2, p3):
                        print(f"possible setting: ({p1}, {p2}, {p3})")
                        matches.append((p1, p2, p3))
                    if tested % 2000 == 0:
                        print(f"tested {tested}/{total}")

        print(f"\nTotal matches found: {len(matches)}")
        return matches
    def candidate_strings(self):
        candidates = []
        matches = self.crack()
        for p1, p2, p3 in matches:
            machine = self.make_machine()
            machine.set_positions(p1, p2, p3)
            decrypted = machine.encrypt(self.ciphertext)
            candidates.append(decrypted)
        return candidates
def make_machine():
    return EnigmaMachine(
        rotors=[
            Rotor('VZBRGITYUPSDNHLXAWMJQOFECK'),
            Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB'),
            Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO')
        ]
    )
print('-' * 20)
text = input("Enter text to encrypt: ")
enigma1 = make_machine()
for _ in range(random.randint(0, 25)):
    enigma1.step()
ciphertext = enigma1.encrypt(text)
print(f"Original text: {text}")
print(f"Enigma Encrypted text: {ciphertext}")
print('-' * 20)
bombe = Bombe(make_machine, crib="WEA", ciphertext=ciphertext)
candidates = bombe.candidate_strings()
print('-' * 20)
print('CANDIDATES:')
for candidate in candidates:
    if candidate == text.upper():
        print(f"***{candidate}***")
    else:
        print(candidate)


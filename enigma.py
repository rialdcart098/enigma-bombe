class Reflector:
    def __init__(self, mapping='EJMZALYXVBWFCRQUONTSPIKHGD'):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.mapping = {self.alphabet[i]: mapping[i] for i in range(26)}
    def forward(self, letter):
        return self.mapping[letter]
    def backward(self, letter):
        for key, value in self.mapping.items():
            if value == letter:
                return key
        return letter
class Rotor:
    def __init__(self, wiring, position=0):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.wiring = wiring
        self.position = position
    def step(self):
        self.position = (self.position + 1) % 26
    def forward(self, letter):
        i = (self.alphabet.index(letter) + self.position) % 26
        return self.wiring[i]
    def backward(self, letter):
        i = self.wiring.index(letter)
        return self.alphabet[(i - self.position) % 26]

class EnigmaMachine:
    def __init__(self, rotors=None):
        self.rotors = rotors if rotors is not None else [
            Rotor('EKMFLGDQZNTOVYHXWABPCIJURS'),
            Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE'),
            Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO')
        ]
        self.reflector = Reflector()
    def press_key(self, key):
        for rotor in self.rotors:
            key = rotor.forward(key)
        key = self.reflector.forward(key)
        for rotor in self.rotors[::-1]:
            key = rotor.backward(key)
        self.step()
        return key
    # specifically for the Bombe.
    def set_positions(self, p1, p2, p3):
        self.rotors[0].position = p1
        self.rotors[1].position = p2
        self.rotors[2].position = p3
    def encrypt(self, plaintext):
        ciphertext = ''
        for char in plaintext.upper():
            if char.isalpha():
                ciphertext += self.press_key(char)
            else:
                ciphertext += char
        return ciphertext
    def step(self):
        self.rotors[0].step()
        if self.rotors[0].position == 0:
            self.rotors[1].step()
            if self.rotors[1].position == 0:
                self.rotors[2].step()
# enigma = EnigmaMachine()
#
# enigma.set_positions(0, 0, 0)
# cipher = enigma.encrypt("HELLO ELLIOT")
# print(cipher)
# enigma.set_positions(0, 0, 0)
# plain = enigma.encrypt(cipher)
# print(plain)
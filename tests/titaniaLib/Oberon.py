import base64
def Code(inputText=""):
    replacements = {
        "f": "ju", "a": "fa", "r": "su", "m": "ra", "n": "re", "j": "na", 
        "e": "je", "k": "ne", "b": "fe", "h": "ke", "t": "te", "d": "ja", 
        "g": "ka", "s": "ta", "q": "se", "p": "sa", "u": "tu", "z": "ge", 
        "v": "za", "w": "ze", "x": "zu", "y": "ga", "c": "fu", "i": "ku", 
        "o": "ru", "l": "nu", "natu": "ju", "tatu": "su", "rje": "re"
    }

    inputText = inputText.lower()
    for key, value in replacements.items():
        inputText = inputText.replace(key, value)
    return inputText

def Decode(inputText=""):
    replacements = {
        "fa": "a", "fe": "b", "fu": "c", "ja": "d", "je": "e", "ju": "f", 
        "ka": "g", "ke": "h", "ku": "i", "na": "j", "ne": "k", "nu": "l", 
        "ra": "m", "re": "n", "ru": "o", "sa": "p", "se": "q", "su": "r", 
        "ta": "s", "te": "t", "tu": "u", "za": "v", "ze": "w", "zu": "x", 
        "ga": "y", "ge": "z"
    }

    inputText = inputText.lower()
    for key, value in replacements.items():
        inputText = inputText.replace(key, value)
    return inputText

def Hide(key):
    key = Code(key)
    key = base64.b64encode(bytes(key, 'utf-8'))
    key = key.hex()
    return key

def Show(revkey):
    revkey = bytes.fromhex(revkey)
    revkey = base64.b64decode(revkey).decode('ascii')
    revkey = Decode(revkey)
def get_text(datei):
    token_text = list()
    with open(datei, mode="r", encoding="utf-8") as infile:
        read = infile.read()
        for tok in read.split():
            token_text.append(tok)
    return token_text


##############################################
# Lexikon einlesen
# Input:  Dateiname (str)
# Output: Abkuerzungen in geeigneter Datenstruktur

def read_lex(datei):
    token_lex = set()
    with open(datei, mode="r", encoding="utf-8") as infile:
        read = infile.read()
        for tok in read.split():
            token_lex.add(tok)
    return token_lex


##############################################
# Tokengrenzen bestimmen
# Input:  Tokens_orth mit vorlaeufigen Tokengrenzen (list)
#         Abbrev (dict)
#
# Output: Tokens mit korrigierten Tokengrenzen (list)
def tokenize(tokens_orth, abbrev):
    new_tokens = list()

    for tok in tokens_orth:
        context = tokens_orth.index(tok)
        # Wort
        if tok.endswith(".") == False:
            new_tokens.append(tok)

        # Satzterminierend
        else:
            if tok in abbrev:
                new_tokens.append(tok)
            elif tokens_orth[context + 1].islower():
                new_tokens.append(tok)
            else:
                new_tokens.append(tok[:-1])
                new_tokens.append(".")
                if tokens_orth[context].endswith(".") and tokens_orth[context + 1].endswith("."):
                    continue
                else:
                    new_tokens.append("")
    return new_tokens


##############################################
# Tokens ausgeben
# Input: Tokens (list)
# Output: --    (Konsole)

def print_out(tokens):
    for tok in tokens:
        print(tok)


##############################################
# Funktion, die alle weiteren Funktionen aufruft

def run_script(input_text, input_lex):
    # 1. Datei „text.txt“ einlesen
    text = get_text(input_text)

    # 2. Abkuerzungslexikon einlesen
    lex = read_lex(input_lex)
    # 3. Tokengrenzen bestimmen
    token_grenzen = tokenize(text, lex)
    # 4. Tokens ausgeben
    # print_out(text)
    # print_out(lex)
    print_out(token_grenzen)


###########################################################
# Hauptprogramm
###########################################################

if __name__ == "__main__":
    input_text = "french_texts.txt"
    input_lex = "abbrev.lex"
    # Funktion, die alle weiteren Funktionen aufruft
    run_script(input_text, input_lex)

# TicTacToe-Spiel in Python auf der Kommandozeile umgesetzt. Ohne KI, nur ein einfaches "2-Spieler Spiel"
# @author Florian Schönsee
# Matrikelnummer: 94 04 85

# Import vom Python-Regex-Modul
import re

# Konstanten für Spielgröße sowie die Zeichen für ein leeres Feld, Spieler X und Spieler Y
GROESSE = 3
LEER = '-'
SPIELER_X = 'X'
SPIELER_O = 'O'

# Aufbau des Spielbretts
def spielbrett_aufbauen(n):
    spielbrett = {}
    for x in range(n):
        for y in range(n):
            spielbrett[(x, y)] = LEER
    return spielbrett

# Ausgabe des Spielbretts auf der Kommandozeile. In den jeweiligen Zellen des Bretts befinden sich die Koordinaten, die
# die Spieler einzutippen haben
def spielbrett_ausgeben(spielbrett):
    print('\n')
    for coord in sorted(spielbrett.keys()):
        x, y = coord
        if y == 0 and x != 0:           
            print('\n' + '-' * 2* len(spielbrett))
        val = spielbrett[coord]
        if val is not LEER:
            print("  %s  |" % (val), end="")
        else:
            print("(%1d,%1d)|" % (coord), end="")
    print('\n')

# Setzen einer Markierung auf dem Spielbrett
def markierung_setzen(spielbrett, coord, spieler):
    if coord in spielbrett.keys() and spielbrett[coord] is LEER:
        spielbrett[coord] = spieler
        return True
    else:
        return False

# Prüfen ob ein Spieler gewonnen hat: dies ist der Fall, wenn ein Spieler 3 X oder O in einer Reihe hat
# Entweder horizontal, vertikal oder diagonal
def pruefe_gewinnen(spielbrett, GROESSE, spieler):
    for n in range(GROESSE):
        rows = [spielbrett[(x, y)] for x, y in sorted(spielbrett.keys()) if n is x]
        cols = [spielbrett[(x, y)] for x, y in sorted(spielbrett.keys()) if n is y]
        diagonals = [spielbrett[(x, y)] for x, y in sorted(spielbrett.keys()) if x is y]
        if rows.count(spieler) is GROESSE or cols.count(spieler) is GROESSE or diagonals.count(spieler) is GROESSE:
            return True
    return False

def spielbrett_voll(spielbrett):
    return list(spielbrett.values()).count(LEER) == 0

# beendet das spiel, wenn entweder das Brett voll ist oder einer der beiden Spieler gewonnen hat    
def spiel_beendet(spielbrett, GROESSE):
    return spielbrett_voll(spielbrett) or pruefe_gewinnen(spielbrett, GROESSE, SPIELER_X) or pruefe_gewinnen(spielbrett, GROESSE, SPIELER_O)

# prüft, ob die Gewinnbedinungen für einen der Spieler erfüllt sind
def pruefe_gewinner(spielbrett, GROESSE):
    if pruefe_gewinnen(spielbrett, GROESSE, SPIELER_X):
        return SPIELER_X
    elif pruefe_gewinnen(spielbrett, GROESSE, SPIELER_O):
        return SPIELER_O
    elif spielbrett_voll(spielbrett):
        return None 

# test-methode, die überprüft, ob die 
def test():
    spielbrett = spielbrett_aufbauen(GROESSE)
    spielbrett_ausgeben(spielbrett)
    setze_markierungen(spielbrett)
    assert pruefe_gewinnen(spielbrett, GROESSE, SPIELER_X) == True
    assert pruefe_gewinnen(spielbrett, GROESSE, SPIELER_O) == False
    spielbrett_ausgeben(spielbrett)
    spielbrett = spielbrett_aufbauen(GROESSE)
    assert markierung_setzen(spielbrett, (0, 0), SPIELER_O) == True
    assert markierung_setzen(spielbrett, (1, 1), SPIELER_O) == True
    assert markierung_setzen(spielbrett, (2, 2), SPIELER_O) == True
    assert pruefe_gewinnen(spielbrett, GROESSE, SPIELER_O) == True
    spielbrett_ausgeben(spielbrett)
    print('test bestanden')

# Setze die Markierungen auf das Spielbrett
def setze_markierungen(spielbrett):
    assert markierung_setzen(spielbrett, (0, 0), SPIELER_X) == True
    assert markierung_setzen(spielbrett, (0, 0), SPIELER_X) == False
    assert markierung_setzen(spielbrett, (1, 1), SPIELER_O) == True
    assert markierung_setzen(spielbrett, (0, 1), SPIELER_X) == True
    assert markierung_setzen(spielbrett, (0, 2), SPIELER_X) == True

# Definiere einen gültigen Zug
def gueltiger_zug(user_in):
    user_in = user_in.strip()
    matches = re.match(r"[0-9]+\s*,\s*[0-9]+", user_in) 
    if matches is not None:
        return tuple(map(int, user_in.split(',')))
    else:
        return False
# Prüfe, ob die Spieler sich an die Regeln halten
def pruefe_gueltige_zuege():
    assert gueltiger_zug('3,4') == (3,4)
    assert gueltiger_zug('3,  4') == (3,4)
    assert gueltiger_zug('a,4') == False
    assert gueltiger_zug('33,49') == (33,49)
    assert gueltiger_zug('33 , 49') == (33,49)
    assert gueltiger_zug('fsdfdsf') == False
    assert gueltiger_zug('fsdm,fdsf') == False

# Das eigentliche Spiel -  die Main-Methode des Programms
if __name__ == '__main__':
    test()
    GROESSE = 3 
    spielbrett = spielbrett_aufbauen(GROESSE)
    print('Willkommen zum Tic Tac Toe Spiel')
    print('Zwei Spieler, X und O - es sind immer die Koordinaten des jeweiligen Feldes anzugeben')
    spielbrett_ausgeben(spielbrett)
    aktiver_spieler = SPIELER_O
    while(not spiel_beendet(spielbrett, GROESSE)):
        user_in = input('Spieler " +  aktiver_spieler + ", du bist dran: ')
        coord = gueltiger_zug(user_in)
        if coord and markierung_setzen(spielbrett, coord, aktiver_spieler):
            spielbrett_ausgeben(spielbrett)
            aktiver_spieler = SPIELER_X  if aktiver_spieler is SPIELER_O else SPIELER_O
        else:
            print('Ungültiger Zug.')
    winner = pruefe_gewinner(spielbrett, GROESSE)
    if winner is not None:
        print('spiel beendet! Spieler %s hat gewonnen!' % winner)
    else: 
        print('Unentschieden. :)')

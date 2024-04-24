import os
from pathlib import Path
import sqlite3
workdir = Path(__file__).parent
database = workdir / 'Telefonbuch.db'

def main():
    einträge = ["Eintrag hinzufügen", "Eintrag suchen", "Nach Rufnummer suchen",
                "Eintrag löschen", "Eintrag ändern", "Inhalt ausgeben", "Ende"]
    while True:
        print("Telefonbuch")
        print("Bitte wählen Sie:")
        for n, i in enumerate(einträge, 1):
            print(f"{n} - i")
            try:
                auswahl = int(input("Ihre Anzahl: "))
                if auswahl > len(einträge) or auswahl < 1:
                    raise ValueError
            except ValueError:
                print("Auswahl ungültig!")
            except KeyboardInterrupt:
                print("Abbruch durch User!")
                ende()
            match auswahl:
                case 1:
                    eintrag_hinzufügen()
                case 2:
                    eintrag_suchen(menü=True)
                case 3:
                    nach_rufnummer_suchen()
                case 4:
                    eintrag_löschen()
                case 5:
                    eintrag_ändern()
                case 6:
                    alle_einträge_ausgeben()
                case 7:
                    ende()
def eintrag_hinzufügen():
    while True:
        try:
            varvorname = input("Bitte geben Sie den Vornamen ein: ")
            varnachname = input("Bitte geben Sie den Nachnamen ein: ")
            varvorwahl = input("Bitte geben Sie die Vorwahl ein: ")
            varrufnummer = input("Bitte geben Sie die Rufnummer ein: ")
            if varvorname == "" or varvorname.upper() == "NULL":
                if varnachname == "" or varnachname.upper() == "NULL":
                    print("Vorname und Nachname dürfen nicht beide leer sein!")
                    continue
                else:
                    varvorname = "NULL"
            if varnachname == "" or varnachname.upper() == "NULL":
                varnachname = "NULL"
            break
        except KeyboardInterrupt:
            print("Abbruch durch User!")
            return main()
    with sqlite3.connect(database) as conn:
        c = conn.cursor()
        params = (varvorname, varnachname, varvorwahl, varrufnummer)
        sql = """INSERT INTO telefonbuch (vorname, nachname, vorwahl, rufnummer) VALUES (?, ?, ?, ?);"""
        c.execute(sql, params)
        conn.commit()
        print("Eintrag wurde erfolgreich erstellt!")
    return main()
def eintrag_suchen(menü=False):
    try:
        varvorname = input("Bitte geben Sie den Vornamen ein: ")
        if varvorname == "":
            varvorname = "%"
        varnachname = input("Bitte geben Sie den Nachnamen ein: ")
        if varnachname == "":
            varnachname = "%"
    except KeyboardInterrupt:
        print("Abbruch durch User!")
        return main()
    with sqlite3.connect(database) as conn:
        c = conn.cursor()
        params = (varvorname, varnachname)
        sql = """SELECT * FROM telefonbuch WHERE vorname LIKE ? AND nachname LIKE ?;"""
        ergebnis = c.execute(sql, params).fetchall()
        print()
        for i in ergebnis:
            print(i[0], i[1], i[2], [3], i[4])
    if menü:
        return main()
    else:
        return ergebnis
def nach_rufnummer_suchen():
    print("Suche nach Rufnummer")
    try:
        varvorwahl = input("Bitte geben Sie die Vorwahl ein: ")
        if varvorwahl == "":
            varvorwahl = "%"
        varrufnummer = input("Bitte geben Sie die Rufnummer ein: ")
        if varrufnummer == "":
            varrufnummer = "%"
    except KeyboardInterrupt:
        print("Abbruch durch User!")
        return main()
    with sqlite3.connect(database) as conn:
        c = conn.cursor()
        params = (varvorwahl, varrufnummer)
        sql = """SELECT * FROM telefonbuch WHERE vorwahl LIKE ? AND rufnummer LIKE ?;"""
        ergebnis = c.execute(sql, params).fetchall()
        print()
        for i in ergebnis:
            print(i[0], i[1], i[2], [3], i[4])
        weiter = input("ENTER drücken zu fortfahren oder \"ä\" zum Ändern eines Eintrags: ").lower()
        print()
    if weiter == "":
        return nach_rufnummer_suchen()
    elif weiter == "ä":
        while True:
            try:
                nr = int(input("Welcher Eintrag soll geändert werden? "))
                return eintrag_ändern(nr)
            except ValueError:
                print("Ungültige Auswahl!")
    else:
        return main()
def eintrag_löschen():
    print("Eintrag löschen")
    ergebnis = eintrag_suchen()
    try:
        nr = int(input("Welcher Eintrag soll gelöscht werden? ID: "))
        for i in ergebnis:
            if i[0] == nr:
                with sqlite3.connect(database) as conn:
                    c = conn.cursor()
                    params = (nr,)
                    sql = """DELETE FROM telefonbuch WHERE ID = ?;"""
                    c.execute(sql, params)
                    conn.commit()
                    print("Eintrag wurde erfolgreich gelöscht!")
                return main()
        raise ValueError()
    except ValueError:
        print("Ungültige Eingabe!")
        print("Es wurde nichts gelöscht!")
        return main()
def alle_einträge_ausgeben():
    with sqlite3.connect(database) as conn:
        c = conn.cursor()
        sql = """SELECT * FROM telefonbuch;"""
        ergebnis = c.execute(sql).fetchall()
        print()
        for i in ergebnis:
            print(i[0], i[1], i[2], [3], i[4])
        print()
    return main()
def eintrag_ändern(nr):
    with sqlite3.connect(database) as conn:
        c = conn.cursor()
        varvorname = input("Bitte geben Sie den neuen Vornamen ein (leerlassen um keine Änderungen vorzunehmen): ")
        if varvorname != "":
            sql = """UPDATE telefonbuch SET vorname = ? WHERE ID = ?;"""
            params = (varvorname, nr)
            c.execute(sql, params)
            conn.commit()
        varnachname = input("Bitte geben Sie den neuen Nachnamen ein (leerlassen um keine Änderungen vorzunehmen): ")
        if varnachname != "":
            sql = """UPDATE telefonbuch SET nachname = ? WHERE ID = ?;"""
            params = (varnachname, nr)
            c.execute(sql, params)
            conn.commit()
        varvorwahl = input("Bitte geben Sie die neue Vorwahl ein (leerlassen um keine Änderungen vorzunehmen): ")
        if varvorwahl != "":
            sql = """UPDATE telefonbuch SET vorwahl = ? WHERE ID = ?;"""
            params = (varvorwahl, nr)
            c.execute(sql, params)
            conn.commit()
        varrufnummer = input("Bitte geben Sie die neue Rufnummer ein (leerlassen um keine Änderungen vorzunehmen): ")
        if varrufnummer != "":
            sql = """UPDATE telefonbuch SET rufnummer = ? WHERE ID = ?;"""
            params = (varrufnummer, nr)
            c.execute(sql, params)
            conn.commit()
        if varvorname == "" and varnachname == "" and varvorwahl == "" and varrufnummer == "":
            print("Es wurde nichts geändert!")
        else:
            print("Eintrag wurde erfolgreich geändert!")
    return main()
def ende():
    print("Auf Wiedersehen!")
    exit(0)
def check_database():
    if not Path.exists(database):
        create_database()
def create_database():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql = """CREATE TABLE telefonbuch(
    ID INTEGER PRIMARY KEY,
    vorname TEXT,
    nachname TEXT,
    vorwahl TEXT,
    rufnummer TEXT);"""
    c.execute(sql)
    conn.commit()
    conn.close()
    print(database, "wurde erfolgreich erstellt!")
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
if __name__ == "main":
    check_database()
    main()
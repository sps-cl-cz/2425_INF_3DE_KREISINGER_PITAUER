import argparse
import os
import hashlib
import glob

# Vytvoření parseru
parser = argparse.ArgumentParser()


#přidání příkazů
def AddArguments():
    parser.add_argument(
        "init",
        action="store_true",
        help="vytvoří nový soubor obsahující list se sledovanými soubory."
    )

    parser.add_argument(
        "add",
        type=str,
        help="Přidá specifikované soubory ke sledování."
    )

    parser.add_argument(
        "remove",
        type=str,
        help="Odebere specifikované soubory ze sledování."
    )
    parser.add_argument(
        "status",
        action="store_true",
        help="zobrazí stav všech sledovaných souborů"
    )
    



#použití argumentů
def main ():
    if args.name:  
        print(f"Ahoj, {args.name}!")
    elif args.init:
        fileName = "output.check"
        # Odstranění existujícího souboru
        if os.path.exists(fileName):
            try:
                os.remove(fileName)  
                print(f"Existující soubor '{fileName}' byl odstraněn.")
            except Exception as e:
                print(f"Chyba při mazání souboru: {e}")
        # Vytvoření nového prázdného souboru
        try:
            with open(fileName, "w") as file:
                pass
            print(f"Nový soubor '{fileName}' byl úspěšně vytvořen.")
        except Exception as e:
            print(f"Chyba při vytváření souboru: {e}")
    else:
        print("Použijte příkaz -h pro nápovědu.")   

AddArguments()
args = parser.parse_args()        
main()


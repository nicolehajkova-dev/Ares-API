import requests

#Vyhledání podle IČO
def hledat_podle_ico():
    ico = input("Zadejte IČO subjektu: ").strip()
    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        obchodni_jmeno = data.get("obchodniJmeno", "Neznámé jméno")
        adresa = data.get("sidlo", {}).get("textovaAdresa", "Neznámá adresa")

        print(f"\n{obchodni_jmeno}\n{adresa}\n")

    except requests.exceptions.RequestException as e:
        print(f"Chyba při získávání dat: {e}")
    except ValueError:
        print("Chybná odpověď serveru nebo nesprávný formát dat.")

#Vyhledání podle názvu
def hledat_podle_nazvu():
    nazev = input("Zadejte název subjektu nebo jeho část: ").strip()
    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    data = {"obchodniJmeno": nazev}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        vysledky = response.json()

        pocet = vysledky.get("pocetCelkem", 0)
        subjekty = vysledky.get("ekonomickeSubjekty", [])

        print(f"\nNalezeno subjektů: {pocet}")
        for subjekt in subjekty:
            jmeno = subjekt.get("obchodniJmeno", "Neznámý název")
            ico = subjekt.get("ico", "Neznámé IČO")
            print(f"{jmeno}, {ico}")

    except requests.exceptions.RequestException as e:
        print(f"Chyba při získávání dat: {e}")
    except ValueError:
        print("Chybná odpověď serveru nebo nesprávný formát dat.")

#Spuštění programu
print("1. Vyhledat podle IČO")
print("2. Vyhledat podle názvu subjektu")
volba = input("Zadejte volbu (IČO nebo název): ").strip()

if volba == "IČO":
    hledat_podle_ico()
elif volba == "název":
    hledat_podle_nazvu()
else:
    print("Neplatná volba.")
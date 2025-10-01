import pprint
def carica_da_file(file_path):
    try:
        with open(file_path,"r",encoding="utf-8") as f:
            numero_sezioni = int(f.readline())
            lista = []
            libro = f.readline()
            while libro != "":
                nuovo_libro = libro.rstrip().split(",")
                lista.append(nuovo_libro)
                libro = f.readline()
            dizionario = {}
            for i in lista:
                if i[4] not in dizionario:
                    dizionario[i[4]]=[i]
                else:
                    dizionario[i[4]].append(i)
            pprint.pprint(dizionario)
        return dizionario, numero_sezioni
    except FileNotFoundError:
        return None



def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path,numero_sezioni):
    nuovo_libro = [titolo,autore,anno,pagine,sezione]
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for key, val in biblioteca.items():
                for libro in val:
                    if (titolo in libro and autore in libro and anno in libro) or (int(sezione) > numero_sezioni):
                        return None
                    else:
                        biblioteca[sezione].append(nuovo_libro)
                        f.write(f"{titolo},{autore},{anno},{pagine},{sezione}\n")
    except FileNotFoundError:
        return None
    return biblioteca





def main():
    biblioteca = []
    file_path = "biblioteca.csv"
    sezioni_presenti = 0

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca,sezioni_presenti = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, str(anno), str(pagine), str(sezione), file_path,sezioni_presenti)
            if libro:
                print(f"Il Libro {titolo} è stato aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()


import pprint
def carica_da_file(file_path):
    try:
        with open(file_path,"r",encoding="utf-8") as f:
            numero_sezioni = int(f.readline())  ##leggo numero delle sezioni disonibili
            lista = []
            libro = f.readline()
            while libro != "":
                nuovo_libro = libro.rstrip().split(",")
                lista.append(nuovo_libro)
                libro = f.readline()
            dizionario = {}             ###per la struttura dati ho deciso di utilizzare un dizionario
            for i in lista:             ###{numero_sezione : lista di liste dove ogni sottolista é un libro appartenente a quella sezione}
                if i[4] not in dizionario:
                    dizionario[i[4]]=[i]
                else:
                    dizionario[i[4]].append(i)
            pprint.pprint(dizionario)
        return dizionario, numero_sezioni     ##restituisco anche la prima riga del file in modo tale da poter verificare
    except FileNotFoundError:                ##se un eventuale libro da aggiungere abbia a se attribuito un numero di sezione
        return None                          ##>>di quello disponibile dalla libreria



def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione,file_path,numero_sezioni):
    nuovo_libro = [titolo,autore,anno,pagine,sezione]
    try:
        with open(file_path, "r",encoding="utf-8") as infile:
            lista_totale = []
            for line in infile:                           ##visto che dovrei controllare ogni singola sezione del dizionario
                libro = line.strip().split(",")        ####per verificare che non ci sia già una copia del libro, risulta agevole
                lista_totale.append(libro)            ####inserire il contenuto del file in una lista di liste per poter controllare ogni libro agevolmente
    except FileNotFoundError: return None

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            if int(numero_sezioni)>=int(sezione):        ##verifico disponibilità sezioni
                if nuovo_libro not in lista_totale:       ##se il libro non è presente lo aggiungo...
                    biblioteca[sezione].append(nuovo_libro)
                    f.write(f"{titolo},{autore},{anno},{pagine},{sezione}\n")  ##...e sovrascrivo il file in modalità append
                    return True
                else:
                    return None               ##se il libro è già presente nella lista totale dei libri
            else:
                return None                ##se la sezione presente eccede la disponibilità della biblioteca
    except FileNotFoundError:
        return None                        ##nel caso in cui il file non sia trovato


def cerca_libro(biblioteca,titolo):
    for key in biblioteca:
        lista = biblioteca[key]
        for i in lista:
            if i[0]==titolo:            ##itero su ogni libro di ogni sezione
                libro = i
                return libro          ##se il libro viene trovato restituisco subito i valori corrispondenti
            else:                   ##se il titolo non è uguale passo al prossimo e una volta terminati quelli di una sezione
                pass                 ##passo a quella dopo
    return None                   ##nel caso in cui non venga trovato restituisco None


def elenco_libri_sezione_per_titolo(biblioteca, sezione,sezioni_presenti):
    if int(sezione)<=int(sezioni_presenti):   ##il numero della sezione deve essere compreso nella
        lista_libri = biblioteca[f"{sezione}"]   ##disponibilità della biblioteca
        lista_ordinata = sorted(lista_libri, key=lambda x: x[0])
        return lista_ordinata
    else:                              ##uso una funzione lambda per riordinare la lista di liste in base al titolo
        return None                    ##in ordine alfabetico

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

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione,sezioni_presenti)
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


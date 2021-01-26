# cinema
## System zarządzania kinem, Bazy Danych 2020-2021


### Opis
Na głównej stronie znajduje się harmonogram seansów na najbliższy tydzień. Na główną stronę można dostać się klikając zakładkę "schedule".  
  
Można też wyszukiwać filmy (zakładka "movies") oraz seanse (zakładka "showings").

Aby zamówić bilet, trzeba posiadać konto. Są trzy rodzaje kont:
* klient - podstawowe konto, pozwala na zamawianie biletów
* kasjer - rozszerzenie konta klienta, pozwala na akceptowanie zamówień w zakładce "profile"
* pracownik - rozszerzenie konta klienta, pozwala na zarządzanie kinem (dodawanie seansów, filmów, sal kinowych) oraz kasjerami (pozwala dodać/usunąć kasjera) w zakładce "staff panel".
  
Swoje aktualne bilety, ich stan oraz historię biletów można znaleźć w zakładce profilu "profile".

### Technologia
Projekt stworzony przy użyciu:  
* Django
* PostgreSql
* Bootstrap 4

### Baza Danych
Diagram, skrypt tworzący, wyzwalacz oraz funkcja znajdują się w folderze "database".  
Komunikacja z bazą danych jest przy pomocy Django ORM, wszystkie modele są w plikach models.py w poszczegolnych aplikacjach (cinema, orders, users).

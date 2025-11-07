Documento di Specifica dei Requisiti Software (SRS)

Azienda – Gruppo di lavoro\n\n\n\n
Nome azienda: D&G Softwarehouse
Reparto interno: Ufficio Tecnico e Sviluppo
Membri:
• Davide Dolce – Tecnico e sviluppatore software
• Marco Guarinoni – Project Manager

Nome del Progetto
Forza 4

Categoria
Applicazione desktop (eventualmente adattabile a versione web in futuro)

Revisione documento:
Data: 31/10/2025
Versione: 1.0
Da: Davide Dolce, Marco Guarinoni.

1. Introduzione

1.1 Scopo
Lo scopo del progetto è lo sviluppo di un software interattivo del gioco Forza 4, che permetta a due giocatori
di sfidarsi in locale su un’interfaccia grafica intuitiva. Il programma dovrà gestire automaticamente le regole del gioco,
determinare il vincitore e consentire una nuova partita in modo immediato.

1.2 Pubblico di destinazione
Il software è destinato a studenti e appassionati di giochi da tavolo digitali, scuole e docenti per l’utilizzo didattico, 
e utenti che desiderano un passatempo rapido e intelligente.

1.3 Valore del prodotto
Il prodotto offre un’esperienza di gioco fluida, grafica semplice ma funzionale e codice modulare utile per scopi didattici.

1.4 Ambito
Il software consente di giocare a Forza 4 in modalità 1 contro 1 locale, visualizzare la griglia e le pedine in tempo 
reale, determinare vittorie o pareggi e resettare la partita. Non è prevista una modalità online né salvataggio dello 
stato della partita.

2. Requisiti funzionali
• Mostrare una griglia 7x6.
• Permettere ai due giocatori di inserire, a turno, la propria pedina colorata.
• Segnalare la vittoria quando un giocatore allinea 4 pedine orizzontalmente, verticalmente o diagonalmente.
• Gestire le condizioni di pareggio.
• Consentire di ricominciare la partita.
• Visualizzare messaggi informativi (es. “Turno del giocatore 1”).
• Fornire un’interfaccia grafica con menu principale e area di gioco.

3. Requisiti non funzionali
3.1 Correttezza
Il sistema deve seguire le regole ufficiali di Forza 4 e garantire risultati coerenti.
3.2 Prestazioni
Il tempo di risposta alle azioni dell’utente deve essere inferiore a 0,2 secondi.
3.3 Affidabilità
Il software non deve bloccarsi durante l’esecuzione normale; tasso di errore <1%.
3.4 Robustezza
Il sistema deve gestire input non validi senza crash.
3.5 Scalabilità
Progetto estendibile a modalità CPU (contro un bot).
3.6 Sicurezza
Non sono richieste misure avanzate di sicurezza.
3.7 Usabilità
Interfaccia chiara, intuitiva e adatta anche a utenti non esperti.

4. Integrazione di terze parti
------------------------------------------------------------------------------|
software di terze   |      utilizzo         | informazioni  | obbligatorio/   |
parti               |                       | aggiuntive    | facoltativo     |
--------------------|-----------------------|-------------  |-----------------|
python              |  interfaccia grafica  |creazione GUI  | obbligatorio    |
--------------------|-----------------------|-------------- |-----------------|
github              |  versionamento codice | gestione del  |                 |
                    |                       | progetto      |obbligatorio     |
------------------------------------------------------------------------------|

5. Strumenti software
5.1 Ambienti di sviluppo: Visual Studio Code / IntelliJ IDEA
5.2 Sistemi di controllo delle versioni: Git e GitHub
5.3 Editor di database: non applicabile
5.4 Strumenti per il test: Debugger IDE, test manuali di partita
5.5 Framework: python

6. Scadenze
Inizio sviluppo: 19/10/2025
Presentazione: 14/11/2025
Data di fine progetto: 23/01/2026

7. Definizioni e acronimi
GUI: Graphical User Interface
IDE: Integrated Development Environment
SRS: Software Requirement Specification

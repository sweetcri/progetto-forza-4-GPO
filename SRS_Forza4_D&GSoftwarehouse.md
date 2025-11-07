Documento di Specifica dei Requisiti Software (SRS)<br><br>

Azienda – Gruppo di lavoro<br>
Nome azienda: D&G Softwarehouse<br>
Reparto interno: Ufficio Tecnico e Sviluppo<br>
Membri:<br>
• Davide Dolce – Tecnico e sviluppatore software<br>
• Marco Guarinoni – Project Manager<br><br>

Nome del Progetto<br>
Forza 4<br><br>

Categoria<br>
Applicazione desktop (eventualmente adattabile a versione web in futuro)<br><br>

Revisione documento:<br>
Data: 31/10/2025<br>
Versione: 1.0<br>
Da: Davide Dolce, Marco Guarinoni.<br><br>

1. Introduzione<br><b><br>

1.1 Scopo<br>
Lo scopo del progetto è lo sviluppo di un software interattivo del gioco Forza 4, che permetta a due giocatori<br>
di sfidarsi in locale su un’interfaccia grafica intuitiva. Il programma dovrà gestire automaticamente le regole del gioco,<br>
determinare il vincitore e consentire una nuova partita in modo immediato.<br><br>

1.2 Pubblico di destinazione<br>
Il software è destinato a studenti e appassionati di giochi da tavolo digitali, scuole e docenti per l’utilizzo didattico, <br>
e utenti che desiderano un passatempo rapido e intelligente.<br><br>

1.3 Valore del prodotto<br>
Il prodotto offre un’esperienza di gioco fluida, grafica semplice ma funzionale e codice modulare utile per scopi didattici.<br><br>

1.4 Ambito<br>
Il software consente di giocare a Forza 4 in modalità 1 contro 1 locale, visualizzare la griglia e le pedine in tempo <br>
reale, determinare vittorie o pareggi e resettare la partita. Non è prevista una modalità online né salvataggio dello <br>
stato della partita.<br><br>

2. Requisiti funzionali<br>
• Mostrare una griglia 7x6.<br>
• Permettere ai due giocatori di inserire, a turno, la propria pedina colorata.<br>
• Segnalare la vittoria quando un giocatore allinea 4 pedine orizzontalmente, verticalmente o diagonalmente.<br>
• Gestire le condizioni di pareggio.<br>
• Consentire di ricominciare la partita.<br>
• Visualizzare messaggi informativi (es. “Turno del giocatore 1”).<br>
• Fornire un’interfaccia grafica con menu principale e area di gioco.<br><br>

3. Requisiti non funzionali<br>
3.1 Correttezza<br>
Il sistema deve seguire le regole ufficiali di Forza 4 e garantire risultati coerenti.<br>
3.2 Prestazioni<br>
Il tempo di risposta alle azioni dell’utente deve essere inferiore a 0,2 secondi.<br>
3.3 Affidabilità<br>
Il software non deve bloccarsi durante l’esecuzione normale; tasso di errore <1%.<br>
3.4 Robustezza<br>
Il sistema deve gestire input non validi senza crash.<br>
3.5 Scalabilità<br>
Progetto estendibile a modalità CPU (contro un bot).<br>
3.6 Sicurezza<br>
Non sono richieste misure avanzate di sicurezza.<br>
3.7 Usabilità<br>
Interfaccia chiara, intuitiva e adatta anche a utenti non esperti.<br><br>

4. Integrazione di terze parti<br>

| software di terze parti      | utilizzo                  | informazioni aggiuntive      | obbligatorio/facoltativo|
|:----------------------------:|:-------------------------:|:----------------------------:|:-----------------------:|
| python                       |  interfaccia grafica      | creazione GUI                |obbligatorio
| github                       |  versionamento codice     | gestione del progetto        |obbligatorio

5. Strumenti software<br>
5.1 Ambienti di sviluppo: Visual Studio Code / IntelliJ IDEA<br>
5.2 Sistemi di controllo delle versioni: Git e GitHub<br>
5.3 Editor di database: non applicabile<br>
5.4 Strumenti per il test: Debugger IDE, test manuali di partita<br>
5.5 Framework: python<br><br>

6. Scadenze<br>
Inizio sviluppo: 19/10/2025<br>
Presentazione: 14/11/2025<br>
Data di fine progetto: 23/01/2026<br><br>

7. Definizioni e acronimi<br>
GUI: Graphical User Interface<br>
IDE: Integrated Development Environment<br>
SRS: Software Requirement Specification

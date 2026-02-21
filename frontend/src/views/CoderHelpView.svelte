<section class="card">
  <h2>Coder help (solo Master)</h2>
  <p>Questa guida è pensata per chi parte da zero: fai copia/incolla dei percorsi e segui i passi in ordine.</p>

  <h3>Tecnologie usate</h3>
  <ul>
    <li><strong>Django (backend):</strong> è il "motore" lato server che gestisce utenti, API e admin. Qui vive la logica account/login. File principali in <code>backend/</code>.</li>
    <li><strong>Django Ninja (API):</strong> crea endpoint semplici tipo <code>/api/auth/login</code>. Riceve dati JSON e risponde JSON. File: <code>backend/core/api.py</code>.</li>
    <li><strong>Svelte + Vite (frontend):</strong> è l'interfaccia visuale con pagine e bottoni. Qui decidi cosa l'utente vede in base al ruolo. File principali in <code>frontend/src/</code>.</li>
    <li><strong>SQLite (database):</strong> è il file dove salvi utenti e profili. Non devi configurare server esterni per iniziare. È usato automaticamente da Django.</li>
  </ul>

  <h3>Dove mettere cosa</h3>
  <ul>
    <li><strong>Pagine UI:</strong> crea file in <code>frontend/src/views/</code>, poi collegali in <code>App.svelte</code> e <code>NavTabs.svelte</code>. Se è pagina solo Master, mostrala con controllo <code>isMaster</code>.</li>
    <li><strong>Componenti riusabili:</strong> mettili in <code>frontend/src/components/</code>. Usali per menu, card, blocchi ripetuti. Così non duplichi codice in più pagine.</li>
    <li><strong>Media statici frontend:</strong> metti immagini/file in <code>frontend/public/media/</code>. Si aprono poi come <code>/media/nomefile</code> dal browser.</li>
    <li><strong>API backend:</strong> aggiungi endpoint in <code>backend/core/api.py</code> e schemi in <code>backend/core/schemas.py</code>. Se salvi dati, crea o aggiorna modelli in <code>backend/core/models.py</code>.</li>
    <li><strong>Media backend:</strong> i file caricati dal server usano <code>backend/media/</code>. URL base già pronta in settings: <code>MEDIA_URL = '/media/'</code>.</li>
  </ul>

  <h3>Come creare una nuova funzionalità (procedura breve)</h3>
  <ol>
    <li><strong>Passo 1:</strong> crea endpoint backend (lettura/salvataggio) e testalo da browser o test. Prima fai funzionare i dati, poi l'interfaccia.</li>
    <li><strong>Passo 2:</strong> aggiungi metodo in <code>frontend/src/lib/api/client.ts</code> per chiamare l'endpoint. Mantieni nomi chiari: <code>getX</code>, <code>createX</code>, <code>updateX</code>.</li>
    <li><strong>Passo 3:</strong> crea o aggiorna pagina in <code>views</code>, collega bottoni/form e mostra messaggi di successo/errore. L'utente deve capire sempre cosa è successo.</li>
  </ol>

  <h3>Regole semplici per ruoli e permessi</h3>
  <ul>
    <li><strong>Controllo UI:</strong> nascondi tab e link sensibili se non Master. Esempio: Coder help e Django admin visibili solo con <code>isMaster = true</code>.</li>
    <li><strong>Controllo backend:</strong> non fidarti solo dell'interfaccia, ricontrolla il ruolo anche nelle API importanti. Questo evita accessi non autorizzati via chiamate manuali.</li>
    <li><strong>Sessione:</strong> dopo login, l'utente resta autenticato grazie ai cookie. Quando fai logout, azzera stato UI e torna al Main menu.</li>
  </ul>

  <h3>Best practice (ultra pratiche)</h3>
  <ul>
    <li>Una pagina = uno scopo chiaro, senza "mega pagina" con tutto dentro.</li>
    <li>Ogni feature nuova: almeno un test backend minimo (status code + campi risposta).</li>
    <li>Se rinomini un campo (es. <code>isMaster</code>), aggiorna subito backend + frontend insieme.</li>
  </ul>
</section>

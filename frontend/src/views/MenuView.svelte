<script lang="ts">
  import { apiClient } from '../lib/api/client';
  import { activeView, authUser } from '../stores/appState';

  let signupUsername = '';
  let signupPassword = '';
  let signupIsMaster = false;

  let loginUsername = '';
  let loginPassword = '';

  let feedback = '';
  let loading = false;

  async function createAccount() {
    loading = true;
    feedback = '';
    try {
      const response = await apiClient.signup(signupUsername, signupPassword, signupIsMaster);
      authUser.set(response.user);
      feedback = 'Account creato e login effettuato.';
      activeView.set('player');
    } catch (error) {
      feedback = error instanceof Error ? error.message : 'Errore durante la creazione account.';
    } finally {
      loading = false;
    }
  }

  async function doLogin() {
    loading = true;
    feedback = '';
    try {
      const response = await apiClient.login(loginUsername, loginPassword);
      authUser.set(response.user);
      feedback = 'Login effettuato con successo.';
      activeView.set('player');
    } catch (error) {
      feedback = error instanceof Error ? error.message : 'Errore durante il login.';
    } finally {
      loading = false;
    }
  }

  async function doLogout() {
    loading = true;
    feedback = '';
    try {
      const response = await apiClient.logout();
      authUser.set(response.user);
      activeView.set('menu');
      feedback = 'Logout effettuato.';
    } catch (error) {
      feedback = error instanceof Error ? error.message : 'Errore durante il logout.';
    } finally {
      loading = false;
    }
  }
</script>

<section class="card">
  <h2>Main menu</h2>

  {#if $authUser.isAuthenticated}
    <p>Connesso come: <strong>{$authUser.username}</strong></p>
    <p>Ruolo: {$authUser.isMaster ? 'Master' : 'Player'}</p>

    {#if $authUser.isMaster}
      <p><a href="http://127.0.0.1:8000/admin/" target="_blank" rel="noreferrer">Apri Django Admin</a></p>
    {/if}

    <button on:click={doLogout} disabled={loading}>Logout</button>
  {:else}
    <div class="grid-two">
      <form on:submit|preventDefault={createAccount}>
        <h3>Crea account</h3>
        <label>Username</label>
        <input bind:value={signupUsername} required minlength="3" />
        <label>Password</label>
        <input type="password" bind:value={signupPassword} required minlength="4" />
        <label>
          <input type="checkbox" bind:checked={signupIsMaster} />
          Crea come Master (isMaster)
        </label>
        <button type="submit" disabled={loading}>Crea e accedi</button>
      </form>

      <form on:submit|preventDefault={doLogin}>
        <h3>Login</h3>
        <label>Username</label>
        <input bind:value={loginUsername} required />
        <label>Password</label>
        <input type="password" bind:value={loginPassword} required />
        <button type="submit" disabled={loading}>Entra</button>
      </form>
    </div>
  {/if}

  {#if feedback}
    <p>{feedback}</p>
  {/if}
</section>

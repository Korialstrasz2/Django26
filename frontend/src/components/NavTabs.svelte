<script lang="ts">
  import { activeView, authUser, type ViewName } from '../stores/appState';

  export let onOpenSettings: () => void;

  function switchView(next: ViewName) {
    activeView.set(next);
  }
</script>

<nav class="top-nav">
  <div class="nav-left">
    <button on:click={() => switchView('menu')}>Main menu</button>
    <button class="icon-button" aria-label="Apri impostazioni" title="Impostazioni" on:click={onOpenSettings}>
      ⚙️
    </button>
  </div>

  <div>
    <button on:click={() => switchView('player')} disabled={!$authUser.isAuthenticated}>Player</button>
    {#if $authUser.isMaster}
      <button on:click={() => switchView('coderHelp')}>Coder help</button>
    {/if}
  </div>
</nav>

<script lang="ts">
  import { activeView, authUser, type ViewName } from '../stores/appState';

  function switchView(next: ViewName) {
    activeView.set(next);
  }
</script>

<nav>
  <button on:click={() => switchView('menu')}>Main menu</button>
  <button on:click={() => switchView('player')} disabled={!$authUser.isAuthenticated}>Player</button>
  {#if $authUser.isMaster}
    <button on:click={() => switchView('coderHelp')}>Coder help</button>
  {/if}
</nav>

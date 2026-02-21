<script lang="ts">
  import { activeView, type ViewName } from '../stores/appState';

  function switchView(next: ViewName) {
    activeView.set(next);
  }
</script>

<nav>
  <button on:click={() => switchView('menu')}>Menu</button>
  <button on:click={() => switchView('player')}>Player</button>
</nav>

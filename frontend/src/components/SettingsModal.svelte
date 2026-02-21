<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { UserSettings } from '../lib/api/client';

  export let isOpen = false;
  export let settings: UserSettings;
  export let saving = false;
  export let cacheClearing = false;
  export let feedback = '';

  let selected = '';

  const dispatch = createEventDispatcher<{
    close: void;
    save: { folder: string };
    clearCache: void;
  }>();

  $: if (isOpen) {
    selected = settings?.selectedStyleFolder || '';
  }
</script>

{#if isOpen}
  <button class="overlay" type="button" aria-label="Chiudi impostazioni" on:click={() => dispatch('close')}>
    <div class="modal" role="dialog" aria-modal="true" aria-label="Impostazioni">
      <h2>Impostazioni</h2>
      <p>Seleziona uno stile sfondo (cartella in <code>media/Immagini/backgrounds/stili</code>).</p>

      <label for="style-folder">Stile</label>
      <select id="style-folder" bind:value={selected}>
        {#each settings.availableStyleFolders as folder}
          <option value={folder}>{folder}</option>
        {/each}
      </select>

      <div class="actions">
        <button on:click={() => dispatch('save', { folder: selected })} disabled={saving || !selected}>
          {saving ? 'Salvataggio...' : 'Salva stile'}
        </button>
        <button class="danger" on:click={() => dispatch('clearCache')} disabled={cacheClearing}>
          {cacheClearing ? 'Pulizia cache...' : 'Svuota cache locale'}
        </button>
        <button on:click={() => dispatch('close')}>Chiudi</button>
      </div>

      {#if feedback}
        <p>{feedback}</p>
      {/if}
    </div>
  </button>
{/if}

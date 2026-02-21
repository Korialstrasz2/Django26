<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import NavTabs from './components/NavTabs.svelte';
  import SettingsModal from './components/SettingsModal.svelte';
  import CoderHelpView from './views/CoderHelpView.svelte';
  import MenuView from './views/MenuView.svelte';
  import { activeView, authUser, latestPing, userSettings, wsStatus } from './stores/appState';
  import { apiClient, type HelloPayload } from './lib/api/client';
  import { getCachedHello, setCachedHello } from './lib/db';
  import { connectPingSocket, closePingSocket } from './lib/ws/pingSocket';
  import { CACHE_VERSION, needsCacheReset } from './lib/cache/cacheVersion';

  let PlayerView: typeof import('./views/PlayerView.svelte').default | null = null;
  let helloData: HelloPayload | null = null;
  let error = '';
  let settingsModalOpen = false;
  let settingsSaving = false;
  let cacheClearing = false;
  let settingsFeedback = '';
  let lastSettingsUser = '';

  async function initCacheVersioning() {
    const previous = localStorage.getItem('cacheVersion');
    if (needsCacheReset(previous)) {
      localStorage.setItem('cacheVersion', CACHE_VERSION);
    }
  }

  async function loadHello() {
    const cached = await getCachedHello();
    if (cached) {
      helloData = cached;
    }

    try {
      const fresh = await apiClient.getHello();
      helloData = fresh;
      await setCachedHello(fresh);
    } catch (err) {
      error = err instanceof Error ? err.message : 'unknown error';
    }
  }

  async function loadCurrentUser() {
    try {
      authUser.set(await apiClient.getCurrentUser());
    } catch {
      authUser.set({ username: '', isAuthenticated: false, isMaster: false });
    }
  }

  async function loadSettings() {
    if (!$authUser.isAuthenticated) {
      userSettings.set({ selectedStyleFolder: '', availableStyleFolders: [], backgrounds: {} });
      return;
    }

    try {
      const settings = await apiClient.getSettings();
      userSettings.set(settings);
    } catch (err) {
      settingsFeedback = err instanceof Error ? err.message : 'Errore caricamento impostazioni';
    }
  }

  async function saveSettings(folder: string) {
    settingsSaving = true;
    settingsFeedback = '';
    try {
      const settings = await apiClient.updateSettings(folder);
      userSettings.set(settings);
      settingsFeedback = 'Stile aggiornato.';
    } catch (err) {
      settingsFeedback = err instanceof Error ? err.message : 'Errore salvataggio impostazioni';
    } finally {
      settingsSaving = false;
    }
  }

  async function clearClientCache() {
    cacheClearing = true;
    settingsFeedback = '';
    try {
      await apiClient.requestCacheClear();
      localStorage.clear();
      sessionStorage.clear();
      if ('caches' in window) {
        const keys = await caches.keys();
        await Promise.all(keys.map((key) => caches.delete(key)));
      }
      settingsFeedback = 'Cache locale eliminata. Ricarica la pagina.';
    } catch (err) {
      settingsFeedback = err instanceof Error ? err.message : 'Errore durante pulizia cache';
    } finally {
      cacheClearing = false;
    }
  }

  function sectionBackground(): string {
    const bg = $userSettings.backgrounds;
    if (!bg) return '';
    if ($activeView === 'menu') return apiClient.toAbsoluteMediaUrl(bg.menu || '');
    if ($activeView === 'player') return apiClient.toAbsoluteMediaUrl(bg.diario || '');
    return apiClient.toAbsoluteMediaUrl(bg.dadi || '');
  }

  onMount(async () => {
    await initCacheVersioning();
    await loadHello();
    await loadCurrentUser();
    await loadSettings();
    connectPingSocket();
  });

  $: if (!$authUser.isAuthenticated && $activeView === 'player') {
    activeView.set('menu');
  }

  $: if (!$authUser.isMaster && $activeView === 'coderHelp') {
    activeView.set('menu');
  }

  $: if ($activeView === 'player' && !PlayerView) {
    import('./views/PlayerView.svelte').then((module) => {
      PlayerView = module.default;
    });
  }

  $: if ($authUser.isAuthenticated && $authUser.username !== lastSettingsUser) {
    lastSettingsUser = $authUser.username;
    loadSettings();
  }

  $: if (!$authUser.isAuthenticated && lastSettingsUser) {
    lastSettingsUser = '';
    userSettings.set({ selectedStyleFolder: '', availableStyleFolders: [], backgrounds: {} });
  }

  onDestroy(() => {
    closePingSocket();
  });
</script>

<main>
  <h1>LAN Multiplayer Hello World</h1>
  <NavTabs onOpenSettings={() => (settingsModalOpen = true)} />

  <SettingsModal
    isOpen={settingsModalOpen}
    settings={$userSettings}
    saving={settingsSaving}
    cacheClearing={cacheClearing}
    feedback={settingsFeedback}
    on:close={() => (settingsModalOpen = false)}
    on:save={(event) => saveSettings(event.detail.folder)}
    on:clearCache={clearClientCache}
  />

  <section class="card section-bg" style={`--section-bg-image: url('${sectionBackground()}')`}>
    {#if $activeView === 'menu'}
      <MenuView />
    {:else if $activeView === 'coderHelp' && $authUser.isMaster}
      <CoderHelpView />
    {:else if PlayerView}
      <svelte:component this={PlayerView} />
    {/if}
  </section>

  <section class="card">
    <h3>API Hello Payload</h3>
    {#if helloData}
      <pre>{JSON.stringify(helloData, null, 2)}</pre>
    {:else}
      <p>Loading...</p>
    {/if}
    {#if error}
      <p class="status-offline">{error}</p>
    {/if}
  </section>

  <section class="card">
    <h3>WebSocket</h3>
    <p>
      Status:
      <span class={$wsStatus === 'open' ? 'status-online' : 'status-offline'}>{$wsStatus}</span>
    </p>
    <p>Latest message: {$latestPing}</p>
  </section>
</main>

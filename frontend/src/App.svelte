<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import NavTabs from './components/NavTabs.svelte';
  import CoderHelpView from './views/CoderHelpView.svelte';
  import MenuView from './views/MenuView.svelte';
  import { activeView, authUser, latestPing, wsStatus } from './stores/appState';
  import { apiClient, type HelloPayload } from './lib/api/client';
  import { getCachedHello, setCachedHello } from './lib/db';
  import { connectPingSocket, closePingSocket } from './lib/ws/pingSocket';
  import { CACHE_VERSION, needsCacheReset } from './lib/cache/cacheVersion';

  let PlayerView: typeof import('./views/PlayerView.svelte').default | null = null;
  let helloData: HelloPayload | null = null;
  let error = '';

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

  onMount(async () => {
    await initCacheVersioning();
    await loadHello();
    await loadCurrentUser();
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

  onDestroy(() => {
    closePingSocket();
  });
</script>

<main>
  <h1>LAN Multiplayer Hello World</h1>
  <NavTabs />

  {#if $activeView === 'menu'}
    <MenuView />
  {:else if $activeView === 'coderHelp' && $authUser.isMaster}
    <CoderHelpView />
  {:else if PlayerView}
    <svelte:component this={PlayerView} />
  {/if}

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

<script lang="ts">
  import Playlist from "./lib/Playlist.svelte";
  import { location, Route } from "./simple-svelte-router";
  import { playlist } from "./store";
</script>

<div class="bg-zinc-300 text-white h-screen overflow-hidden">
  <main
    class="flex flex-col max-w-7xl h-full mx-auto shadow-lg shadow-slate-950"
  >
    <header class="flex flex-row bg-slate-950">
      <h1
        class="flex flex-row space-x-2 items-center text-amber-300 text-xl font-bold px-4 py-2 {$playlist !==
        null
          ? 'order-1'
          : ''}"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          aria-hidden="true"
          class="w-6 h-6 fill-current"
          ><path
            d="M4,15H6A2,2 0 0,1 8,17V19H9V17A2,2 0 0,1 11,15H13A2,2 0 0,1 15,17V19H16V17A2,2 0 0,1 18,15H20A2,2 0 0,1 22,17V19H23V22H1V19H2V17A2,2 0 0,1 4,15M11,7L15,10L11,13V7M4,2H20A2,2 0 0,1 22,4V13.54C21.41,13.19 20.73,13 20,13V4H4V13C3.27,13 2.59,13.19 2,13.54V4A2,2 0 0,1 4,2Z"
          /></svg
        >
        <span class={$playlist !== null ? "sr-only md:not-sr-only" : ""}
          >Video Browser</span
        >
      </h1>
      {#if $playlist !== null}
        <a
          href="#/{$playlist.id}"
          class="text-amber-300 text-xl font-bold px-4 py-2 truncate"
          >{$playlist.title}</a
        >
        <span class="flex-1" />
      {/if}
    </header>
    {#if $location.pathComponents.length >= 1 && $location.pathComponents[0] !== ""}
      <Route path="/:pid"><Playlist /></Route>
    {:else}
      <article class="flex-1 p-4 bg-zinc-700">
        <h2 class="text-lg font-bold mb-2">Welcome</h2>
        <p class="mb-2">
          Hello and welcome to the Video Browser. The video browser is designed
          as a simple way for browsing video playlists. However, it does not
          provide a way for discovering playlists.
        </p>
        <p>
          You will need to return to the site that took you here and ask them to
          link to a specific playlist or video.
        </p>
      </article>
    {/if}
  </main>
</div>

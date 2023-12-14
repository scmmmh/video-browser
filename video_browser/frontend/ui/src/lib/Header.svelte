<script lang="ts">
  import { derived } from "svelte/store";
  import { createQuery, type CreateQueryResult } from "@tanstack/svelte-query";
  import { location } from "../simple-svelte-router";
  import Playlist from "../routes/Playlist.svelte";

  const playlistQuery = derived(location, (location) => {
    if (location.pathComponents.pid) {
      return { queryKey: ["playlists", location.pathComponents.pid] };
    } else {
      return { enabled: false };
    }
  });

  const playlist = createQuery(playlistQuery) as CreateQueryResult<
    Playlist,
    Error
  >;
</script>

<header class="flex flex-row bg-slate-950">
  <h1
    class="flex flex-row space-x-2 items-center text-amber-300 text-xl font-bold px-4 py-2 {$playlist.isSuccess
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
  {#if $playlist.isSuccess}
    <a
      href="#/{$playlist.data.id}"
      class="text-amber-300 text-xl font-bold px-4 py-2 truncate"
      >{$playlist.data.title}</a
    >
    <span class="flex-1" />
  {/if}
</header>

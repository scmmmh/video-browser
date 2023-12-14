<script lang="ts">
  import { getContext } from "svelte";
  import { createQuery, type CreateQueryResult } from "@tanstack/svelte-query";
  import Route from "../../simple-svelte-router/Route.svelte";
  import { location } from "../../simple-svelte-router";

  import Placeholder from "../../lib/Placeholder.svelte";
  import PlaylistPage from "./PlaylistPage.svelte";

  const config = getContext("config") as CreateQueryResult<Config, Error>;

  const playlists = createQuery({
    queryKey: ["playlists", ""],
  }) as CreateQueryResult<Playlist[], Error>;
</script>

<div class="flex-1 flex flex-row overflow-hidden">
  <div class="bg-slate-950 h-full shadow-lg shadow-slate-950">
    <h1 tabindex="-1" class="sr-only">Playlists</h1>
    <ul class="h-full overflow-auto py-4">
      {#if $config.isSuccess && $playlists.isSuccess}
        {#each $playlists.data as playlist}
          <li class="mb-4" title={playlist.title}>
            <a
              href="#/playlists/{playlist.id}"
              class="block px-4 border-r-4 {$location.pathComponents.vid &&
              Number.parseInt($location.pathComponents.vid) === playlist.id
                ? 'border-r-amber-300'
                : 'border-r-slate-950'} hover:border-r-amber-300 focus:border-r-amber-300"
            >
              {#if playlist.thumbnail === null}
                <Placeholder
                  height="h-32"
                  width="w-56"
                  extraCss="mb-2"
                  animate={false}
                />
              {:else}
                <span class="block w-56 mb-2">
                  <img
                    src="{$config.data.video_base_url}{playlist.thumbnail}.png"
                    alt=""
                    aria-hidden="true"
                  />
                </span>
              {/if}
              <span class="block w-56 truncate">{playlist.title}</span>
            </a>
          </li>
        {/each}
      {:else}
        <li class="mb-4 px-4">
          <div class="bg-slate-300 rounded h-32 w-56 mb-2 animate-pulse"></div>
          <div class="bg-slate-300 rounded h-6 w-56 animate-pulse">
            <span class="sr-only">Loading playlists. Please wait.</span>
          </div>
        </li>
        <li class="mb-4 px-4">
          <div class="bg-slate-300 rounded h-32 w-56 mb-2 animate-pulse"></div>
          <div class="bg-slate-300 rounded h-6 w-56 animate-pulse"></div>
        </li>
        <li class="mb-4 px-4">
          <div class="bg-slate-300 rounded h-32 w-56 mb-2 animate-pulse"></div>
          <div class="bg-slate-300 rounded h-6 w-56 animate-pulse"></div>
        </li>
      {/if}
    </ul>
  </div>
  <div class="flex-1 overflow-hidden">
    <Route path="/playlists"></Route>
    <Route path="/playlists/:pid"><PlaylistPage /></Route>
  </div>
</div>

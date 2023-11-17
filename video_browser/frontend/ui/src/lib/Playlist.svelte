<script lang="ts">
  import { Route } from "../simple-svelte-router";
  import { config, playlist, playlistVideos, currentVideo } from "../store";
  import Video from "./Video.svelte";

  let notFound = false;
</script>

{#if notFound}
  <div class="mt-4 px-4 py-2 pb-6 h-full">
    <h2 class="text-lg font-bold mb-2">Playlist not found</h2>
    <p class="mb-2">
      Unfortunately the playlist you were looking for could not be found. The
      Video Browser does not provide a way for exploring the available
      playlists. You will need to return to the site that took you here and ask
      them to fix the link to the playlist.
    </p>
  </div>
{:else if $playlist === null}
  <div class="mt-4 px-4 py-2 pb-6 h-full">
    <h2 class="text-lg font-bold mb-2">Loading the playlist data</h2>
  </div>
{:else}
  <article class="flex flex-col sm:flex-row h-full overflow-hidden">
    <nav class="bg-zinc-950">
      <h2 class="sr-only">{$playlist.title}</h2>
      <ul class="flex flex-row sm:flex-col h-full overflow-auto">
        {#each $playlistVideos as video}
          <li class="px-4 sm:px-0 sm:py-4 sm:pl-4">
            <a
              href="#/{$playlist.id}/{video.id}"
              class="flex flex-col overflow-hidden w-48 border-b-4 sm:border-b-0 sm:border-r-4 sm:pr-4 {$currentVideo !==
                null && video.id === $currentVideo.id
                ? 'border-amber-300'
                : 'border-zinc-950'}"
            >
              <img
                src="{$config?.video_base_url}{video.id}.png"
                alt={video.title}
              />
              <span
                class="block mt-2 text-sm truncate {$currentVideo !== null &&
                video.id === $currentVideo.id
                  ? 'font-bold'
                  : ''}">{video.title}</span
              >
            </a>
          </li>
        {/each}
      </ul>
    </nav>
    <Route path="/:pid/:vid"><Video /></Route>
  </article>
{/if}

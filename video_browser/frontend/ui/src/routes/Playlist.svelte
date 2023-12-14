<script lang="ts">
  import { getContext } from "svelte";
  import { derived } from "svelte/store";
  import { location } from "../simple-svelte-router";
  import { createQuery, type CreateQueryResult } from "@tanstack/svelte-query";

  import Status from "../lib/Status.svelte";
  import Placeholder from "../lib/Placeholder.svelte";

  const config = getContext("config") as CreateQueryResult<Config, Error>;

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

  const playlistVideosQuery = derived(location, (location) => {
    if (location.pathComponents.pid) {
      return { queryKey: ["playlists", location.pathComponents.pid, "videos"] };
    } else {
      return { enabled: false };
    }
  });
  const playlistVideos = createQuery(playlistVideosQuery) as CreateQueryResult<
    Video[],
    Error
  >;
</script>

{#if $playlist.isError || $playlistVideos.isError}
  <Status>
    <span slot="title">Playlist not found</span>
    <p slot="message">
      Unfortunately the playlist you were looking for could not be found. The
      Video Browser does not provide a way for exploring the available
      playlists. You will need to return to the site that took you here and ask
      them to fix the link to the playlist.
    </p>
  </Status>
{:else}
  <article
    class="flex-1 flex flex-col p-4 shadow-inner shadow-zinc-950 bg-zinc-700 overflow-hidden"
  >
    <h2 tabindex="-1" class="sr-only">
      {$playlist.isSuccess ? $playlist.data.title : "Playlist loading"}
    </h2>
    <ul
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 auto-rows-min gap-4 h-full overflow-auto"
    >
      <span class="hidden">{$playlistVideos.isSuccess}</span>
      {#if $playlist.isSuccess && $playlistVideos.isSuccess && $config.isSuccess}
        {#each $playlistVideos.data as video}
          <li>
            <a href="#/{$playlist.data.id}/{video.id}">
              <img
                src="{$config.data.video_base_url}{video.id}.png"
                alt={video.title}
                aria-hidden="true"
              />
              <span class="block">{video.title}</span>
            </a>
          </li>
        {/each}
      {:else}
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
        <li>
          <Placeholder width="" height="h-32" extraCss="mb-2" />
          <Placeholder width="" height="h-6" extraCss="mb-2" />
        </li>
      {/if}
    </ul>
  </article>
{/if}

<script lang="ts">
  import { getContext } from "svelte";
  import { createQuery, type CreateQueryResult } from "@tanstack/svelte-query";
  import Route from "../../simple-svelte-router/Route.svelte";
  import { location } from "../../simple-svelte-router";

  import VideoPage from "./VideoPage.svelte";
  import NewVideoPage from "./NewVideoPage.svelte";

  const config = getContext("config") as CreateQueryResult<Config, Error>;

  const videos = createQuery({ queryKey: ["videos", ""] }) as CreateQueryResult<
    Video[],
    Error
  >;
</script>

<div class="flex-1 flex flex-row overflow-hidden">
  <div class="bg-slate-950 h-full shadow-lg shadow-slate-950">
    <h1 tabindex="-1" class="sr-only">Videos</h1>
    <ul class="h-full overflow-auto py-4">
      {#if $config.isSuccess && $videos.isSuccess}
        {#each $videos.data as video}
          <li class="mb-4" title={video.title}>
            <a
              href="#/videos/{video.id}"
              class="block px-4 border-r-4 {$location.pathComponents.vid &&
              Number.parseInt($location.pathComponents.vid) === video.id
                ? 'border-r-amber-300'
                : 'border-r-slate-950'} hover:border-r-amber-300 focus:border-r-amber-300"
            >
              <span class="block h-32 w-56 mb-2"
                ><img
                  src="{$config.data.video_base_url}{video.public_id}.png"
                  alt=""
                  aria-hidden="true"
                /></span
              >
              <span class="block w-56 truncate">{video.title}</span>
            </a>
          </li>
        {/each}
      {:else}
        <li class="mb-4 px-4">
          <div class="bg-slate-300 rounded h-32 w-56 mb-2 animate-pulse"></div>
          <div class="bg-slate-300 rounded h-6 w-56 animate-pulse">
            <span class="sr-only">Loading videos. Please wait.</span>
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
    <Route path="/videos"><NewVideoPage /></Route>
    <Route path="/videos/:vid"><VideoPage /></Route>
  </div>
</div>

<script lang="ts">
  import { getContext, onDestroy, tick } from "svelte";
  import { derived } from "svelte/store";
  import { createQuery, type CreateQueryResult } from "@tanstack/svelte-query";
  import { WebVTTParser } from "webvtt-parser";
  import { location } from "../simple-svelte-router";

  import Placeholder from "../lib/Placeholder.svelte";
  import Status from "../lib/Status.svelte";

  let navListElement: HTMLOListElement | null = null;
  let VideoPlayer: any = null;

  import("../lib/VideoPlayer.svelte").then((module) => {
    VideoPlayer = module.default;
  });

  const config = getContext("config") as CreateQueryResult<Config, Error>;

  const playlistVideosQuery = derived(location, (location) => {
    if (location.pathComponents.pid) {
      return {
        queryKey: ["playlists", location.pathComponents.pid, "videos"],
      };
    } else {
      return { enabled: false };
    }
  });
  const playlistVideos = createQuery(playlistVideosQuery) as CreateQueryResult<
    Video[],
    Error
  >;

  const videoQuery = derived(location, (location) => {
    if (location.pathComponents.vid) {
      return {
        queryKey: ["videos", location.pathComponents.vid],
      };
    } else {
      return { enabled: false };
    }
  });
  const video = createQuery(videoQuery) as CreateQueryResult<Video, Error>;

  const transcriptQuery = derived([location, config], ([location, config]) => {
    if (location.pathComponents.vid && config.isSuccess) {
      return {
        queryKey: ["videos", location.pathComponents.vid, "transcript"],
        queryFn: async () => {
          const response = await window.fetch(
            config.data.video_base_url + location.pathComponents.vid + ".vtt",
          );
          if (response.ok) {
            return response.text();
          }
          throw new Error("Could not load the transcript");
        },
      };
    } else {
      return { enabled: false };
    }
  });
  const transcript = createQuery(transcriptQuery) as CreateQueryResult<
    string,
    Error
  >;
  const parser = new WebVTTParser();
  const transcriptParas = derived(transcript, (transcript) => {
    if (transcript.isSuccess) {
      const vtt = parser.parse(transcript.data);
      let buffer: string[] = [];
      const newParagraphs: string[] = [];
      for (let cue of vtt.cues) {
        if (cue.text.startsWith("[") && cue.text.endsWith("]")) {
          continue;
        } else if (cue.text.endsWith(".")) {
          buffer.push(cue.text);
          newParagraphs.push(buffer.join(" "));
          buffer = [];
        } else {
          buffer.push(cue.text);
        }
      }
      if (buffer.length > 0) {
        newParagraphs.push(buffer.join(""));
      }
      return newParagraphs;
    } else {
      return [];
    }
  });

  function focusCurrentVideo() {
    tick().then(() => {
      if (navListElement !== null) {
        const current = navListElement.querySelector(
          "#playlist-item-" + $location.pathComponents.vid,
        );
        if (current !== null) {
          current.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      }
    });
  }
  const playlistVideosUnsubscribe = playlistVideos.subscribe(focusCurrentVideo);
  const locationUnsubscribe = location.subscribe(focusCurrentVideo);
  onDestroy(() => {
    playlistVideosUnsubscribe();
    locationUnsubscribe();
  });
</script>

{#if $playlistVideos.isSuccess || $playlistVideos.isPending}
  <article
    class="flex-1 flex flex-col md:flex-row shadow-inner shadow-zinc-950 bg-zinc-700 overflow-hidden"
  >
    <nav class="bg-zinc-950">
      <ol
        bind:this={navListElement}
        class="flex flex-row md:flex-col h-full overflow-auto"
      >
        {#if $playlistVideos.isSuccess}
          {#each $playlistVideos.data as video}
            <li
              id="playlist-item-{video.id}"
              class="px-4 sm:px-0 sm:py-4 sm:pl-4"
            >
              <a
                href="#/{$location.pathComponents.pid}/{video.id}"
                class="flex flex-col overflow-hidden w-48 border-b-4 sm:border-b-0 sm:border-r-4 sm:pr-4 {$location
                  .pathComponents.vid === video.id
                  ? 'border-amber-300'
                  : 'border-zinc-950'}"
              >
                {#if $config.isSuccess}
                  <img
                    src="{$config.data.video_base_url}{video.id}.png"
                    alt={video.title}
                  />
                {/if}
                <span
                  class="block mt-2 text-sm truncate {$location.pathComponents
                    .vid === video.id
                    ? 'font-bold'
                    : ''}">{video.title}</span
                >
              </a>
            </li>
          {/each}
        {:else}
          <li>
            <Placeholder height="h-32" width="w-56" extraCss="mb-2" />
            <Placeholder height="h-6" width="w-56" extraCss="mb-4">
              <span class="sr-only">Loading videos. Please wait.</span>
            </Placeholder>
          </li>
          <li>
            <Placeholder height="h-32" width="w-56" extraCss="mb-2" />
            <Placeholder height="h-6" width="w-56" extraCss="mb-4" />
          </li>
          <li>
            <Placeholder height="h-32" width="w-56" extraCss="mb-2" />
            <Placeholder height="h-6" width="w-56" extraCss="mb-4" />
          </li>
        {/if}
      </ol>
    </nav>
    <section class="flex flex-col flex-1 p-4 overflow-hidden">
      {#if $video.isSuccess}
        <h2 class="text-lg font-bold truncate mb-4">
          {$video.data.title}
        </h2>
        <div class="flex-1">
          {#if VideoPlayer !== null}
            <svelte:component this={VideoPlayer} vid={$video.data.id} />
          {:else}
            <Placeholder height="h-[24rem]" width="w-full" extraCss="mb-4" />
          {/if}
        </div>
        <div
          class="max-h-[20%] pt-2 mt-4 border-t border-t-zinc-950 overflow-auto"
        >
          {#if $transcript.isSuccess}
            {#each $transcriptParas as para}
              <p class="mb-2">{para}</p>
            {/each}
          {:else if $transcript.isError}
            <p>Unfortunately the transcript could not be loaded.</p>
          {/if}
        </div>
      {:else if $video.isPending || $transcript.isPending}
        <Placeholder height="h-8" width="w-full" extraCss="mb-4" />
        <Placeholder height="h-[24rem]" width="w-full" extraCss="mb-4" />
        <Placeholder height="h-28" width="w-full" extraCss="mb-4" />
      {:else if $video.isError}
        <Status>
          <span slot="title">Video not found</span>
          <p slot="message">
            Unfortunately the video you were looking for could not be found.
            Please select a different video from the left
          </p>
        </Status>
      {/if}
    </section>
  </article>
{:else if $playlistVideos.isError}
  <Status>
    <span slot="title">Playlist not found</span>
    <p slot="message">
      Unfortunately the playlist you were looking for could not be found. The
      Video Browser does not provide a way for exploring the available
      playlists. You will need to return to the site that took you here and ask
      them to fix the link to the playlist.
    </p>
  </Status>
{/if}
<!--{#if $currentVideo !== null}
  <section
    class="flex-1 flex flex-col p-4 shadow-inner shadow-zinc-950 bg-zinc-700 overflow-hidden"
  >
    <h3 class="sr-only">{$currentVideo.title}</h3>
    <div class="flex-1">
      {#key $location.pathComponents[1]}
        <VideoPlayer vid={$location.pathComponents[1]} />
      {/key}
    </div>
    <div class="h-1/4 overflow-y-auto mt-4 border-t border-zinc-950">
      <h4 class="sr-only">Transcript</h4>
      {#each paragraphs as paragraph}
        <p class="mb-2">{paragraph}</p>
      {/each}
    </div>
  </section>
{/if}-->

<script lang="ts">
  import { derived } from "svelte/store";
  import { createQuery, type CreateQueryResult } from "@tanstack/svelte-query";
  import { location } from "../../simple-svelte-router";
  import { WebVTTParser } from "webvtt-parser";

  import Placeholder from "../../lib/Placeholder.svelte";
  import VideoPlayer from "../../lib/VideoPlayer.svelte";

  const videoQuery = derived(location, (location) => {
    if (location.pathComponents.vid) {
      return { queryKey: ["videos", location.pathComponents.vid] };
    } else {
      return { queryKey: ["videos", "null"] };
    }
  });

  const video = createQuery(videoQuery) as CreateQueryResult<Video, Error>;

  const transcriptQuery = derived(location, (location) => {
    if (location.pathComponents.vid) {
      return {
        queryKey: ["videos", location.pathComponents.vid, "transcript"],
      };
    } else {
      return { queryKey: ["videos", "null", "transcript"] };
    }
  });

  const transcript = createQuery(transcriptQuery) as CreateQueryResult<
    { text: string },
    Error
  >;

  const parser = new WebVTTParser();

  const transcriptParas = derived(transcript, (transcript) => {
    if (transcript.isSuccess) {
      const vtt = parser.parse(transcript.data.text);
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
</script>

<svelte:head
  ><title>{$video.isSuccess ? $video.data.title : "Loading"}</title
  ></svelte:head
>

<div class="flex flex-col bg-zinc-700 h-full px-4 py-4 overflow-hidden">
  {#if $video.isSuccess && $transcript.isSuccess}
    <h1 class="text-xl font-bold mb-4">{$video.data.title}</h1>
    <div class="flex-1 flex flex-row space-x-4 overflow-hidden">
      <div class="w-[42rem]">
        <div class="h-96 mb-4">
          <VideoPlayer vid={$video.data.public_id}></VideoPlayer>
        </div>
        <p>{$video.data.description}</p>
      </div>
      <div class="flex-1 max-w-[32rem] h-full overflow-auto">
        {#each $transcriptParas as para}
          <p class="mb-2">{para}</p>
        {/each}
      </div>
    </div>
  {:else}
    <Placeholder width="w-[42rem]" height="h-10" extraCss="mb-4"
      ><span class="sr-only">Loading. Please wait.</span></Placeholder
    >
    <div class="flex flex-row space-x-4">
      <div class="w-[42rem]">
        <Placeholder width="w-[42rem]" height="h-96" extraCss="mb-4" />
        <Placeholder width="w-[42rem]" height="h-16" />
      </div>
      <div class="flex-1">
        <Placeholder width="w-[32rem]" height="h-[29rem]" />
      </div>
    </div>
  {/if}
</div>

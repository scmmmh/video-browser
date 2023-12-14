<script lang="ts">
  import { onMount, onDestroy, getContext } from "svelte";
  import { type CreateQueryResult } from "@tanstack/svelte-query";
  import videojs from "video.js";

  export let vid: string;
  let videoPlayer: HTMLVideoElement;
  const config = getContext("config") as CreateQueryResult<Config, Error>;

  onDestroy(() => {
    videojs(videoPlayer).dispose();
  });

  onMount(() => {
    videojs(videoPlayer, {
      fill: true,
      responsive: true,
    });
  });
</script>

{#if $config.isSuccess}
  <video
    bind:this={videoPlayer}
    class="video-js bg-transparent"
    controls
    preload="auto"
    poster="{$config.data.video_base_url}{vid}.png"
  >
    <source src="{$config.data.video_base_url}{vid}.mp4" type="video/mp4" />
    <track
      kind="captions"
      src="{$config.data.video_base_url}{vid}.vtt"
      srclang="en"
      label="English"
      default
    />
    <p class="vjs-no-js">
      To view this video please enable JavaScript, and consider upgrading to a
      web browser that
      <a href="https://videojs.com/html5-video-support/" target="_blank"
        >supports HTML5 video</a
      >
    </p>
  </video>
{/if}

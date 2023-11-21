<script lang="ts">
  import { onMount, onDestroy, tick } from "svelte";
  import videojs from "video.js";
  import type Player from "video.js/dist/types/player";

  import { config } from "../store/config";

  export let vid: string;
  let videoPlayer: HTMLVideoElement;

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

<video
  bind:this={videoPlayer}
  class="video-js bg-transparent"
  controls
  preload="auto"
  poster="{$config?.video_base_url}{vid}.png"
>
  <source src="{$config?.video_base_url}{vid}.mp4" type="video/mp4" />
  <track
    kind="captions"
    src="{$config?.video_base_url}{vid}.vtt"
    srclang="en"
    label="English"
    default
  />
  <p class="vjs-no-js">
    To view this video please enable JavaScript, and consider upgrading to a web
    browser that
    <a href="https://videojs.com/html5-video-support/" target="_blank"
      >supports HTML5 video</a
    >
  </p>
</video>

<script lang="ts">
  import videojs from "video.js";
  import type Player from "video.js/dist/types/player";
  import { onDestroy, tick } from "svelte";

  export let vid: string;
  let videoPlayer: HTMLVideoElement;
  let player: Player | null = null;

  onDestroy(() => {
    videojs(videoPlayer).dispose();
    player = null;
  });

  $: {
    if (player) {
      videojs(videoPlayer).dispose();
      player = null;
    }
    tick().then(() => {
      videojs(videoPlayer);
    });
  }
</script>

<video
  bind:this={videoPlayer}
  class="video-js"
  controls
  preload="auto"
  width="1024"
  height="576"
>
  <source src="//localhost:8080/{vid}.mp4" type="video/mp4" />
  <track
    kind="captions"
    src="//localhost:8080/{vid}.vtt"
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

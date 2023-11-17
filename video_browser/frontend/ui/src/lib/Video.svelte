<script lang="ts">
  import { onDestroy } from "svelte";
  import { WebVTTParser } from "webvtt-parser";
  import { location } from "../simple-svelte-router";

  import VideoPlayer from "../lib/VideoPlayer.svelte";
  import { currentVideo, config } from "../store";

  const parser = new WebVTTParser();
  let paragraphs: string[] = [];

  const currentVideoUnsubscribe = currentVideo.subscribe((currentVideo) => {
    if (currentVideo) {
      paragraphs = [];
      window
        .fetch($config?.video_base_url + currentVideo.id + ".vtt")
        .then((response) => {
          if (response.status === 200) {
            response.text().then((data) => {
              const vtt = parser.parse(data);
              let buffer: string[] = [];
              const newParagraphs: string[] = [];
              for (let cue of vtt.cues) {
                if (cue.text.startsWith("[") && cue.text.endsWith("]")) {
                  continue;
                } else if (cue.text.endsWith(".")) {
                  buffer.push(cue.text);
                  newParagraphs.push(buffer.join(""));
                  buffer = [];
                } else {
                  buffer.push(cue.text);
                }
              }
              if (buffer.length > 0) {
                newParagraphs.push(buffer.join(""));
              }
              paragraphs = newParagraphs;
            });
          }
        });
    }
  });

  onDestroy(currentVideoUnsubscribe);
</script>

{#if $currentVideo !== null}
  <section
    class="flex-1 flex flex-col p-4 shadow-inner shadow-zinc-950 bg-zinc-700 overflow-hidden"
  >
    <h3 class="sr-only">{$currentVideo.title}</h3>
    <div class="flex-1">
      <VideoPlayer vid={$location.pathComponents[1]} />
    </div>
    <div class="h-1/4 overflow-y-auto mt-4 border-t border-zinc-950">
      <h4 class="sr-only">Transcript</h4>
      {#each paragraphs as paragraph}
        <p class="mb-2">{paragraph}</p>
      {/each}
    </div>
  </section>
{/if}

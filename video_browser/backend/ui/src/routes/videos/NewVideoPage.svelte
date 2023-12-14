<script lang="ts">
  import { getContext } from "svelte";
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";
  import { location } from "../../simple-svelte-router";

  const getAuthToken = getContext("getAuthToken") as () => string;
  let formElement: HTMLFormElement | null = null;
  const queryClient = useQueryClient();
  const formCreator = createMutation({
    mutationFn: async () => {
      if (formElement !== null) {
        const response = await window.fetch("/api/videos/", {
          method: "POST",
          body: new FormData(formElement),
          headers: {
            Authorization: "Bearer " + getAuthToken(),
          },
        });
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Failed to create the video");
        }
      } else {
        throw new Error("No form found");
      }
    },
    onSuccess(data: Video) {
      queryClient.invalidateQueries({ queryKey: ["videos", ""] });
      location.push("/videos/" + data.id);
    },
  });

  async function uploadVideo(ev: Event) {
    ev.preventDefault();
    if (!$formCreator.isPending) {
      $formCreator.mutate();
    }
  }
</script>

<svelte:head><title>Upload a new Video</title></svelte:head>

<div class="flex flex-col bg-zinc-700 h-full px-4 py-4 overflow-hidden">
  <h1 class="text-xl font-bold mb-4">Upload a new Video</h1>
  <form on:submit={uploadVideo} bind:this={formElement} class="w-96">
    <label class="block mb-4"
      ><span class="block text-sm pb-1">Title</span>
      <input
        name="title"
        type="text"
        class="block px-2 py-1 w-full shadow-inner rounded text-black"
      />
    </label>
    <label class="block mb-4"
      ><span class="block text-sm pb-1">Description</span>
      <input
        name="description"
        type="text"
        class="block px-2 py-1 w-full shadow-inner rounded text-black"
      />
    </label>
    <label class="block mb-4"
      ><span class="block text-sm pb-1">Video File</span>
      <input
        name="video"
        type="file"
        class="block px-2 py-1 w-full shadow-inner rounded"
      />
    </label>
    <label class="block mb-4"
      ><span class="block text-sm pb-1">Poster File</span>
      <input
        name="poster"
        type="file"
        class="block px-2 py-1 w-full shadow-inner rounded"
      />
    </label>
    <label class="block mb-4"
      ><span class="block text-sm pb-1">Transcription File</span>
      <input
        name="transcript"
        type="file"
        class="block px-2 py-1 w-full shadow-inner rounded"
      />
    </label>
    <div class="text-right">
      {#if $formCreator.isPending}
        <span class="inline-block px-3 py-1 rounded bg-amber-300 text-black"
          >Uploading...</span
        >
      {:else}
        <button
          type="submit"
          class="inline-block px-3 py-1 rounded bg-amber-300 text-black"
          >Upload</button
        >
      {/if}
    </div>
  </form>
</div>

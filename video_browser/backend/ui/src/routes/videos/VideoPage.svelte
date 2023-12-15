<script lang="ts">
  import { getContext } from "svelte";
  import { derived } from "svelte/store";
  import {
    createMutation,
    createQuery,
    useQueryClient,
    type CreateQueryResult,
  } from "@tanstack/svelte-query";
  import { location } from "../../simple-svelte-router";
  import { WebVTTParser } from "webvtt-parser";

  import Placeholder from "../../lib/Placeholder.svelte";
  import VideoPlayer from "../../lib/VideoPlayer.svelte";
  import EditableField from "../../lib/EditableField.svelte";
  import ModalDialog from "../../lib/ModalDialog.svelte";
  import Icon from "../../lib/Icon.svelte";
  import { mdiImageEdit, mdiMovieEdit, mdiTextBoxEdit } from "@mdi/js";

  const parser = new WebVTTParser();
  const getAuthToken = getContext("getAuthToken") as () => string;
  const queryClient = useQueryClient();
  let showUpdateFile = false;
  let updateFileTitle = "";
  let updateFileField = "";
  let updateFileForm: HTMLFormElement | null = null;

  const videoQuery = derived(location, (location) => {
    if (location.pathComponents.vid) {
      return { queryKey: ["videos", location.pathComponents.vid] };
    } else {
      return { queryKey: ["videos", "null"], enabled: false };
    }
  });

  const video = createQuery(videoQuery) as CreateQueryResult<Video, Error>;

  const transcriptQuery = derived(location, (location) => {
    if (location.pathComponents.vid) {
      return {
        queryKey: ["videos", location.pathComponents.vid, "transcript"],
      };
    } else {
      return { queryKey: ["videos", "null", "transcript"], enabled: false };
    }
  });

  const transcript = createQuery(transcriptQuery) as CreateQueryResult<
    { text: string },
    Error
  >;

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

  const videoUpdater = createMutation({
    mutationFn: async (formData: FormData) => {
      const response = await window.fetch(
        "/api/videos/" + $location.pathComponents.vid,
        {
          method: "PATCH",
          body: formData,
          headers: { Authorization: "Bearer " + getAuthToken() },
        },
      );
      if (response.ok) {
        return response.json();
      }
      throw new Error("Failed to update the video");
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["videos"] });
      showUpdateFile = false;
    },
  });

  function updateTitle(ev: CustomEvent) {
    const formData = new FormData();
    formData.set("title", ev.detail);
    $videoUpdater.mutate(formData);
  }

  function updateDescription(ev: CustomEvent) {
    const formData = new FormData();
    formData.set("description", ev.detail);
    $videoUpdater.mutate(formData);
  }

  function updateFile(ev: Event) {
    ev.preventDefault();
    if (updateFileForm) {
      $videoUpdater.mutate(new FormData(updateFileForm));
    }
  }
</script>

<svelte:head
  ><title>{$video.isSuccess ? $video.data.title : "Loading"}</title
  ></svelte:head
>

<div
  class="relative flex flex-col bg-zinc-700 h-full px-4 py-4 overflow-hidden"
>
  {#if $video.isSuccess && $transcript.isSuccess}
    <h1 class="text-xl font-bold mb-4">
      <EditableField on:change={updateTitle} value={$video.data.title} />
    </h1>
    <div class="flex-1 flex flex-row space-x-4 overflow-hidden">
      <div class="w-[42rem]">
        <div class="relative h-96 mb-4">
          <div class="absolute top-0 right-0 z-10 flex flex-row space-x-2">
            <button
              on:click={() => {
                showUpdateFile = true;
                updateFileTitle = "Update this video's poster";
                updateFileField = "poster";
              }}
              class="p-2 rounded bg-amber-300 text-black"
            >
              <Icon
                path={mdiImageEdit}
                title="Upload a new version of the poster"
                class="w-6 h-6"
              />
            </button>
            <button
              on:click={() => {
                showUpdateFile = true;
                updateFileTitle = "Update this video";
                updateFileField = "video";
              }}
              class="p-2 rounded bg-amber-300 text-black"
            >
              <Icon
                path={mdiMovieEdit}
                title="Upload a new version of this video"
                class="w-6 h-6"
              />
            </button>
          </div>
          <VideoPlayer vid={$video.data.public_id}></VideoPlayer>
        </div>
        <p>
          <EditableField
            on:change={updateDescription}
            value={$video.data.description}
          />
        </p>
      </div>
      <div class="relative flex-1 max-w-[32rem] h-full overflow-auto">
        <div class="sticky top-0 z-10 flex flex-row space-x-2 justify-end">
          <button
            on:click={() => {
              showUpdateFile = true;
              updateFileTitle = "Update this video's transcript";
              updateFileField = "transcript";
            }}
            class="p-2 rounded bg-amber-300 text-black"
          >
            <Icon
              path={mdiTextBoxEdit}
              title="Upload a new version of the transcript"
              class="w-6 h-6"
            />
          </button>
        </div>
        {#each $transcriptParas as para}
          <p class="mb-2">{para}</p>
        {/each}
      </div>
    </div>
    {#if showUpdateFile}
      <ModalDialog>
        <span slot="title">{updateFileTitle}</span>
        <form bind:this={updateFileForm} on:submit={updateFile} slot="content">
          <label class="block mb-4">
            <span class="block text-sm">New file</span>
            <input name={updateFileField} type="file" />
          </label>
          <div class="flex flex-row justify-end space-x-2">
            <button
              on:click={() => {
                showUpdateFile = false;
              }}
              type="button"
              class="p-2 rounded bg-red-500 text-white"
            >
              Don't update
            </button>
            <button type="submit" class="p-2 rounded bg-green-500 text-white">
              Update
            </button>
          </div>
        </form>
      </ModalDialog>
    {/if}
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

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
  import {
    mdiArrowDownBold,
    mdiArrowUpBold,
    mdiPlusThick,
    mdiTrashCan,
  } from "@mdi/js";

  import Placeholder from "../../lib/Placeholder.svelte";
  import Icon from "../../lib/Icon.svelte";

  const getAuthToken = getContext("getAuthToken") as () => string;
  const queryClient = useQueryClient();
  let addVideoId = "-1";

  const playlistQuery = derived(location, (location) => {
    if (location.pathComponents.pid) {
      return { queryKey: ["playlists", location.pathComponents.pid] };
    } else {
      return { queryKey: ["playlists", "null"], enabled: false };
    }
  });

  const playlist = createQuery(playlistQuery) as CreateQueryResult<
    Playlist,
    Error
  >;

  const videosQuery = derived(location, (location) => {
    if (location.pathComponents.pid) {
      return { queryKey: ["playlists", location.pathComponents.pid, "videos"] };
    } else {
      return { queryKey: ["playlists", "null", "videos"], enabled: false };
    }
  });

  const videos = createQuery(videosQuery) as CreateQueryResult<Video[], Error>;

  const allVideos = createQuery({
    queryKey: ["videos", ""],
  }) as CreateQueryResult<Video[], Error>;

  const addableVideos = derived([videos, allVideos], ([videos, allVideos]) => {
    if (videos.isSuccess && allVideos.isSuccess) {
      const videoIds = videos.data.map((video) => {
        return video.id;
      });
      return allVideos.data.filter((video) => {
        return videoIds.indexOf(video.id) < 0;
      });
    }
    return [];
  });

  const videosUpdater = createMutation({
    mutationFn: async (videos: Video[]) => {
      const response = await window.fetch(
        "/api/playlists/" + $location.pathComponents.pid + "/videos",
        {
          method: "PUT",
          body: JSON.stringify(videos),
          headers: {
            Authorization: "Bearer " + getAuthToken(),
            "Content-Type": "application/json",
          },
        },
      );
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to update the playlist");
      }
    },
    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: ["playlists", $location.pathComponents.pid],
      });
    },
  });

  function moveVideo(video: Video, direction: number) {
    if ($videos.isSuccess) {
      const newVideos = $videos.data.slice();
      const videoIdx = newVideos.indexOf(video);
      newVideos.splice(videoIdx, 1);
      if (direction < 0) {
        newVideos.splice(videoIdx + direction, 0, video);
      } else if (direction > 0) {
        newVideos.splice(videoIdx + direction, 0, video);
      }
      $videosUpdater.mutate(newVideos);
    }
  }

  function addVideo(ev: Event) {
    ev.preventDefault();
    if ($addableVideos.length > 0 && $videos.isSuccess) {
      const videoId = Number.parseInt(addVideoId);
      const newVideos = $videos.data.slice();
      for (let video of $addableVideos) {
        if (video.id === videoId) {
          newVideos.push(video);
        }
      }
      $videosUpdater.mutate(newVideos);
    }
  }
</script>

<svelte:head
  ><title>{$playlist.isSuccess ? $playlist.data.title : "Loading"}</title
  ></svelte:head
>

<div class="flex flex-col bg-zinc-700 h-full px-4 py-4 overflow-hidden">
  {#if $playlist.isSuccess && $videos.isSuccess}
    <h1 class="text-xl font-bold mb-4">{$playlist.data.title}</h1>
    <ol>
      {#each $videos.data as video, idx}
        <li class="flex flex-row items-center">
          {#if idx > 0}
            <button
              on:click={() => {
                moveVideo(video, -1);
              }}
              class="px-1 py-1"
            >
              <Icon
                path={mdiArrowUpBold}
                title="Move this video further up in the playlist"
                class="w-6 h-6 text-amber-300"
              />
            </button>
          {:else}
            <span class="block px-1 py-1">
              <Icon
                path={mdiArrowUpBold}
                title="The first video in the playlist cannot be moved further up"
                class="w-6 h-6 text-slate-300"
              />
            </span>
          {/if}
          {#if idx < $videos.data.length - 1}
            <button
              on:click={() => {
                moveVideo(video, 1);
              }}
              class="px-1 py-1"
            >
              <Icon
                path={mdiArrowDownBold}
                title="Move this video further down in the playlist"
                class="w-6 h-6 text-amber-300"
              />
            </button>
          {:else}
            <span class="block px-1 py-1">
              <Icon
                path={mdiArrowDownBold}
                title="The last video in the playlist cannot be moved further down"
                class="w-6 h-6 text-slate-300"
              />
            </span>
          {/if}
          <button
            on:click={() => {
              if (
                confirm(
                  "Please confirm you wish to remove the video from the playlist",
                )
              ) {
                moveVideo(video, 0);
              }
            }}
            class="px-1 py-1"
          >
            <Icon
              path={mdiTrashCan}
              title="Remove this video from the playlist"
              class="w-6 h-6 text-amber-300"
            />
          </button>
          <span class="ml-4">{video.title}</span>
        </li>
      {/each}
    </ol>
    {#if $addableVideos.length > 0}
      <h2 class="mt-8 mb-4 font-bold text-lg">Add a Video</h2>
      <form on:submit={addVideo} class="flex flex-row">
        <label>
          <span class="sr-only">Select the video to add</span>
          <select
            bind:value={addVideoId}
            class="block h-full bg-white text-black px-3 py-2 rounded-l"
          >
            {#each $addableVideos as video}
              <option value={video.id}>{video.title}</option>
            {/each}
          </select>
        </label>
        <button
          type="submit"
          class="inline-block px-3 py-2 rounded-r bg-amber-300 text-black"
        >
          <Icon
            title="Add the selected video"
            path={mdiPlusThick}
            class="w-6 h-6 text-black"
          />
        </button>
      </form>
    {/if}
  {:else}
    <Placeholder width="w-[42rem]" height="h-10" extraCss="mb-4"
      ><span class="sr-only">Loading. Please wait.</span></Placeholder
    >
    <Placeholder width="w-[42rem]" height="h-6" extraCss="mb-2" />
    <Placeholder width="w-[42rem]" height="h-6" extraCss="mb-2" />
    <Placeholder width="w-[42rem]" height="h-6" extraCss="mb-2" />
    <Placeholder width="w-[42rem]" height="h-6" extraCss="mb-2" />
  {/if}
</div>

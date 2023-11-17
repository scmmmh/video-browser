import { derived } from "svelte/store";
import { location } from "../simple-svelte-router";
import { playlistVideos } from "./playlist";

export const currentVideo = derived([location, playlistVideos], ([location, playlistVideos]) => {
  if (location.pathComponents.length === 2) {
    for (let video of playlistVideos) {
      if (video.id === location.pathComponents[1]) {
        return video;
      }
    }
  }
  return null;
}, null as Video | null);

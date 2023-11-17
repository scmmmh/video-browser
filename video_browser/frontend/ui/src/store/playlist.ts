
import { derived } from "svelte/store";
import { location } from "../simple-svelte-router";

import { config } from "./config";

export const playlist = derived([location, config], ([location, config], set) => {
  if (config !== null) {
    window.fetch(
      "/api/playlists/" + location.pathComponents[0]
    ).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          set(data as Playlist);
        })
      }
    });
  }
}, null as Playlist | null);

export const playlistVideos = derived(playlist, (playlist, set) => {
  if (playlist !== null) {
    window.fetch("/api/playlists/" + playlist.id + "/videos").then((response) => {
      if (response.status === 200) {
        response.json().then((videos) => { set(videos as Video[]) });
      } else {
        set([]);
      }
    })
  } else {
    set([]);
  }
}, [] as Video[]);

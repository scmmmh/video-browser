/// <reference types="svelte" />
/// <reference types="vite/client" />

type Config = {
  video_base_url: string,
};

type Playlist = {
  id: string,
  title: string,
  description: string,
  videos: string[],
};

type Video = {
  id: string,
  title: string,
  description: string,
};

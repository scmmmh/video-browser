/// <reference types="svelte" />
/// <reference types="vite/client" />

type Config = {
  video_base_url: string,
};

type User = {
  id: number,
  email: string,
  name: string,
};

type Video = {
  id: number,
  public_id: string,
  title: string,
  description: string,
};

import { writable } from "svelte/store";

export const config = writable(null as Config | null);

window.fetch("/api/").then((response) => {
  if (response.status === 200) {
    response.json().then((data) => {
      config.set(data as Config);
    });
  }
});

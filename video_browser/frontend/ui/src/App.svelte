<script lang="ts">
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
  import { Route } from "./simple-svelte-router";

  import ConfigLoader from "./lib/ConfigLoader.svelte";
  import Header from "./lib/Header.svelte";
  import Playlist from "./routes/Playlist.svelte";
  import Video from "./routes/Video.svelte";

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        queryFn: async ({ queryKey }) => {
          const response = await window.fetch("/api/" + queryKey.join("/"));
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("An error occurred (" + response.status + ")", {
              cause: await response.json(),
            });
          }
        },
      },
    },
  });
</script>

<QueryClientProvider client={queryClient}>
  <div class="bg-zinc-300 text-white h-screen overflow-hidden">
    <ConfigLoader>
      <main
        class="flex flex-col max-w-7xl h-full mx-auto shadow-lg shadow-slate-950"
      >
        <Header />
        <Route path="/">
          <article class="flex-1 p-4 bg-zinc-700">
            <h2 class="text-lg font-bold mb-2">Welcome</h2>
            <p class="mb-2">
              Hello and welcome to the Video Browser. The video browser is
              designed as a simple way for browsing video playlists. However, it
              does not provide a way for discovering playlists.
            </p>
            <p>
              You will need to return to the site that took you here and ask
              them to link to a specific playlist or video.
            </p>
          </article>
        </Route>
        <Route path="/:pid"><Playlist /></Route>
        <Route path="/:pid/:vid"><Video /></Route>
      </main>
    </ConfigLoader>
  </div>
</QueryClientProvider>

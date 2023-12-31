<script lang="ts">
  import { setContext } from "svelte";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
  import { sessionPreferences, type NestedStorage } from "./preferences";

  import Route from "./simple-svelte-router/Route.svelte";
  import LandingPage from "./routes/LandingPage.svelte";
  import Authenticate from "./lib/Authenticate.svelte";
  import ConfigLoader from "./lib/ConfigLoader.svelte";
  import Header from "./lib/Header.svelte";
  import VideosPage from "./routes/videos/VideosPage.svelte";
  import PlaylistsPage from "./routes/playlists/PlaylistsPage.svelte";

  let authToken =
    $sessionPreferences.auth &&
    ($sessionPreferences.auth as NestedStorage).token
      ? ($sessionPreferences.auth as NestedStorage).token
      : "";
  setContext("setAuthToken", (newToken: string) => {
    authToken = newToken;
    sessionPreferences.setPreference("auth.token", newToken);
  });
  setContext("getAuthToken", () => {
    return authToken;
  });

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        queryFn: async ({ queryKey }) => {
          const response = await window.fetch("/api/" + queryKey.join("/"), {
            headers: { Authorization: "Bearer " + authToken },
          });
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
  <ConfigLoader>
    <div
      class="flex flex-col bg-zinc-300 text-white w-screen h-screen overflow-hidden"
    >
      <Authenticate>
        <Header />
        <Route path="/"><LandingPage /></Route>
        <Route path="/videos/*"><VideosPage /></Route>
        <Route path="/playlists/*"><PlaylistsPage /></Route>
      </Authenticate>
    </div>
  </ConfigLoader>
</QueryClientProvider>

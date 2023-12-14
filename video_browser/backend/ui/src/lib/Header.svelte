<script lang="ts">
  import { getContext } from "svelte";
  import {
    createQuery,
    useQueryClient,
    type CreateQueryResult,
  } from "@tanstack/svelte-query";
  import { location } from "../simple-svelte-router";

  const user = createQuery({
    queryKey: ["auth", "user"],
  }) as CreateQueryResult<User, Error>;
  const queryClient = useQueryClient();
  const setAuthToken = getContext("setAuthToken") as (newToken: string) => void;

  function logout() {
    setAuthToken("");
    queryClient.invalidateQueries({ queryKey: ["auth", "user"] });
    queryClient.resetQueries({ queryKey: ["auth", "user"] });
  }
</script>

<div class="bg-slate-950 text-white shadow-lg shadow-slate-950">
  <ul class="flex flex-row space-x-4 pt-1">
    <li>
      <a
        href="#/"
        class="block px-3 py-1 text-amber-300 font-bold border-b-4 {$location.pathname ===
        '/'
          ? 'border-b-amber-300'
          : 'border-b-slate-950'} hover:border-b-amber-300 focus:border-b-amber-300"
        >Video Browser</a
      >
    </li>
    <li>
      <a
        href="#/videos"
        class="block px-3 py-1 text-amber-300 font-bold border-b-4 {$location.pathname.startsWith(
          '/videos',
        )
          ? 'border-b-amber-300'
          : 'border-b-slate-950'} hover:border-b-amber-300 focus:border-b-amber-300"
        >Videos</a
      >
    </li>
    <li>
      <a
        href="#/playlists"
        class="block px-3 py-1 text-amber-300 font-bold border-b-4 {$location.pathname.startsWith(
          '/playlists',
        )
          ? 'border-b-amber-300'
          : 'border-b-slate-950'} hover:border-b-amber-300 focus:border-b-amber-300"
        >Playlists</a
      >
    </li>
    <li class="flex-1"></li>
    {#if $user.isSuccess}
      <li>
        <span class="block px-3 py-1 text-amber-300 font-bold"
          >{$user.data.name}</span
        >
      </li>
    {/if}
    <li>
      <button
        on:click={logout}
        class="block px-3 py-1 text-amber-300 font-bold border-b-4 border-b-slate-950 hover:border-b-amber-300 focus:border-b-amber-300"
        >Logout</button
      >
    </li>
  </ul>
</div>

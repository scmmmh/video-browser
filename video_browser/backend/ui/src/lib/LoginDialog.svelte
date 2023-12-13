<script lang="ts">
  import { onMount, getContext } from "svelte";
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";

  type LoginData = {
    email: string;
    password: string;
  };

  let headerElement: HTMLHeadingElement | null = null;
  const queryClient = useQueryClient();
  const authData = { email: "", password: "" };
  const setAuthToken = getContext("setAuthToken") as (newToken: string) => void;

  const authenticator = createMutation({
    mutationFn: async (loginData: LoginData) => {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(loginData),
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) {
        throw new Error("Authentication failed");
      }
      return response.text();
    },
    onSuccess(data) {
      setAuthToken(data);
      queryClient.invalidateQueries({ queryKey: ["auth", "user"] });
    },
  });

  function login(ev: Event) {
    ev.preventDefault();
    if (!$authenticator.isPending) {
      $authenticator.mutate(authData);
    }
  }

  onMount(() => {
    if (headerElement) {
      headerElement.focus();
    }
  });
</script>

{#if $authenticator.isSuccess}
  <div
    role="dialog"
    class="absolute left-1/2 top-1/2 w-96 transform -translate-x-1/2 -translate-y-1/2 bg-zinc-700 text-white shadow-lg shadow-slate-950 rounded"
  >
    <h1
      bind:this={headerElement}
      tabindex="-1"
      class="px-3 py-1 rounded-t bg-slate-950 text-amber-300 text-lg font-bold"
    >
      Loading user data...
    </h1>
    <p class="px-3 pt-3 pb-2">
      The system is currently loading your user data. Please wait...
    </p>
  </div>
{:else}
  <div
    role="dialog"
    class="absolute left-1/2 top-1/2 w-96 transform -translate-x-1/2 -translate-y-1/2 bg-zinc-700 text-white shadow-lg shadow-slate-950 rounded"
  >
    <h1
      bind:this={headerElement}
      tabindex="-1"
      class="px-3 py-1 rounded-t bg-slate-950 text-amber-300 text-lg font-bold"
    >
      Login
    </h1>
    <form class="px-3 pt-3 pb-2" on:submit={login}>
      <label class="block mb-4"
        ><span class="block text-sm pb-1">E-Mail</span>
        <input
          bind:value={authData.email}
          type="email"
          class="block px-2 py-1 w-full shadow-inner rounded text-black"
        />
      </label>
      <label class="block mb-4"
        ><span class="block text-sm pb-1">Password</span>
        <input
          bind:value={authData.password}
          type="password"
          class="block px-2 py-1 w-full shadow-inner rounded text-black"
        />
      </label>
      <div class="text-right">
        {#if $authenticator.isPending}
          <span class="inline-block px-3 py-1 rounded bg-amber-300 text-black"
            >Logging in...</span
          >
        {:else}
          <button
            type="submit"
            class="inline-block px-3 py-1 rounded bg-amber-300 text-black"
            >Log In</button
          >
        {/if}
      </div>
    </form>
  </div>
{/if}

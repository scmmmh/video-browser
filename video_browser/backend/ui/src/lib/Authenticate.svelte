<script lang="ts">
  import { onMount, setContext, createEventDispatcher } from "svelte";
  import {
    createMutation,
    createQuery,
    useQueryClient,
  } from "@tanstack/svelte-query";

  import LoginDialog from "./LoginDialog.svelte";

  type LoginData = {
    email: string;
    password: string;
  };

  const dispatcher = createEventDispatcher();
  let headerElement: HTMLHeadingElement | null = null;
  const queryClient = useQueryClient();
  const authData = { email: "", password: "" };

  const user = createQuery({
    queryKey: ["auth", "user"],
  });
</script>

{#if $user.isSuccess && $user.data}
  <slot />
{:else}<LoginDialog />{/if}

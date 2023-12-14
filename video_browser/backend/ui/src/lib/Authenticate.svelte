<script lang="ts">
  import { createQuery } from "@tanstack/svelte-query";

  import LoginDialog from "./LoginDialog.svelte";

  const user = createQuery({
    queryKey: ["auth", "user"],
  });
</script>

{#if $user.isSuccess && $user.data}
  <slot />
{:else}
  <LoginDialog />
{/if}

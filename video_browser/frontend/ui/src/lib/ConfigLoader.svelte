<script lang="ts">
  import { setContext } from "svelte";
  import { createQuery } from "@tanstack/svelte-query";

  import Status from "./Status.svelte";

  const config = createQuery({ queryKey: [""] });

  setContext("config", config);
</script>

{#if $config.isSuccess}
  <slot />
{:else}
  <Status>
    <span slot="title">Loading the configuration</span>
    <p slot="message">The configuration is being loaded. Please wait.</p>
  </Status>
{/if}

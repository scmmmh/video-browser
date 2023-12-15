<script lang="ts">
  import { createEventDispatcher, tick } from "svelte";
  import { mdiCancel, mdiCheck, mdiPencil } from "@mdi/js";
  import Icon from "./Icon.svelte";

  export let value: string;
  let localValue: string;

  const dispatch = createEventDispatcher();
  let editing: boolean = false;
  let inputElement: HTMLInputElement | null = null;
  let editButtonElement: HTMLButtonElement | null = null;

  function startEditing() {
    editing = true;
    tick().then(() => {
      if (inputElement) {
        inputElement.focus();
      }
    });
  }

  function stopEditing() {
    editing = false;
    localValue = value;
    tick().then(() => {
      if (editButtonElement) {
        editButtonElement.focus();
      }
    });
  }

  function save(ev: Event) {
    ev.preventDefault();
    dispatch("change", localValue);
    stopEditing();
  }

  $: {
    localValue = value;
  }
</script>

{#if editing}
  <form on:submit={save} class="flex flex-row">
    <input
      type="text"
      bind:this={inputElement}
      bind:value={localValue}
      class="px-2 flex-1 text-black rounded-l"
    />
    <button
      on:click={stopEditing}
      type="button"
      class="p-2 bg-red-500 text-white"
    >
      <Icon path={mdiCancel} class="w-6 h-6" title="Edit this field" />
    </button>
    <button type="submit" class="p-2 rounded-r bg-green-500 text-white">
      <Icon path={mdiCheck} class="w-6 h-6" title="Edit this field" />
    </button>
  </form>
{:else}
  <div class="flex flex-row">
    <span class="flex-1">{value}</span>
    <button
      bind:this={editButtonElement}
      on:click={startEditing}
      class="p-2 rounded bg-amber-300 text-black"
    >
      <Icon path={mdiPencil} class="w-6 h-6" title="Edit this field" />
    </button>
  </div>
{/if}

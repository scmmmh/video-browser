<script lang="ts">
  export let path: string;
  export let title: string;
  let cls: string;
  export { cls as class };
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  class="fill-current stroke-current {cls}"
  ><title>{title}</title><path d={path} /></svg
>

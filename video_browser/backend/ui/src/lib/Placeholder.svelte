<script lang="ts">
  export let display: string = "block";
  export let width: string;
  export let height: string;
  export let extraCss: string = "";
</script>

<span
  class="{display} bg-slate-300 rounded {width} {height} animate-pulse {extraCss}"
  ><slot /></span
>

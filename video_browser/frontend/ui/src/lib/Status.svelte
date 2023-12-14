<script lang="ts"></script>

<div
  role="status"
  class="absolute left-1/2 top-1/2 w-96 transform -translate-x-1/2 -translate-y-1/2 bg-zinc-700 text-white shadow-lg shadow-slate-950 rounded"
>
  <div
    class="px-3 py-1 rounded-t bg-slate-950 text-amber-300 text-lg font-bold"
  >
    <slot name="title" />
  </div>
  <div class="px-3 pt-3 pb-2"><slot name="message" /></div>
</div>

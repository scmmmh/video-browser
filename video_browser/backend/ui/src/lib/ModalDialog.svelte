<script lang="ts"></script>

<div class="fixed z-50 top-0 left-0 w-screen h-screen bg-zinc-700/70">
  <div
    role="dialog"
    aria-modal="true"
    class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 bg-zinc-700 shadow-lg shadow-zinc-950"
  >
    <h3
      tabindex="-1"
      class="px-3 py-1 rounded-t bg-slate-950 text-amber-300 text-lg font-bold"
    >
      <slot name="title" />
    </h3>
    <div class="rounded-b px-3 pt-3 pb-2"><slot name="content" /></div>
  </div>
</div>

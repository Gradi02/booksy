<script setup>
defineProps({
  search: String,
});

defineEmits(["update:search"]);
</script>

<template>
  <header class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
    <div class="px-6 py-4 flex items-center justify-between gap-4">
      <div class="flex-1">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Hardware List</h2>
        <div class="relative">
          <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input
            :value="search"
            @input="$emit('update:search', $event.target.value)"
            type="text"
            placeholder="Ask AI…"
            class="w-full md:w-96 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>
    </div>
  </header>
</template>

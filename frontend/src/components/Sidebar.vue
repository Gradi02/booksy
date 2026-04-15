<script setup>
defineProps({
  active: String,
});

defineEmits(["logout"]);
</script>

<template>
  <aside class="w-64 bg-white border-r border-gray-200 shadow-sm overflow-y-auto">
    <!-- Logo Section -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
          🔧
        </div>
        <h1 class="text-xl font-bold text-gray-900">Hardware Manager</h1>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="p-4 space-y-2">
      <a
        href="#"
        :class="[
          'flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
          active === 'hardware'
            ? 'bg-blue-50 text-blue-600'
            : 'text-gray-700 hover:bg-gray-100',
        ]"
      >
        <span class="text-xl">📋</span>
        Hardware List
      </a>
      <a
        href="#"
        :class="[
          'flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
          active === 'rentals'
            ? 'bg-blue-50 text-blue-600'
            : 'text-gray-700 hover:bg-gray-100',
        ]"
      >
        <span class="text-xl">🛒</span>
        My Rentals
      </a>
      <a
        href="#"
        :class="[
          'flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
          active === 'admin'
            ? 'bg-blue-50 text-blue-600'
            : 'text-gray-700 hover:bg-gray-100',
        ]"
      >
        <span class="text-xl">⚙️</span>
        Admin Panel
      </a>
    </nav>

    <!-- Bottom Section -->
    <div class="absolute bottom-0 left-0 right-0 w-64 p-4 border-t border-gray-200">
      <button
        @click="$emit('logout')"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-red-600 hover:bg-red-50 transition-colors"
      >
        <span class="text-xl">🚪</span>
        Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  currentView: String,
});
</script>

<template>
  <header class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
    <div class="px-6 py-4 flex items-center justify-between gap-4">
      <div class="flex-1">
        <h2 class="text-2xl font-bold text-gray-900">
          {{ currentView === 'hardware' ? 'Hardware List' : currentView === 'rentals' ? 'My Rentals' : currentView === 'admin-devices' ? 'Device Management' : currentView === 'admin-users' ? 'User Management' : currentView === 'ai-assistant' ? 'AI Assistant' : 'Hardware Manager' }}
        </h2>
      </div>
    </div>
  </header>
</template>

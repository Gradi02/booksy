<script setup>
defineProps({
  active: String,
  isAdmin: Boolean,
});

defineEmits(["navigate", "logout"]);
</script>

<template>
  <aside class="w-64 bg-white border-r border-gray-200 shadow-sm overflow-y-auto flex flex-col h-screen">
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
    <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
      <!-- User Section -->
      <div class="mb-6">
        <p class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">User</p>
        <button
          @click="$emit('navigate', 'hardware')"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
            active === 'hardware'
              ? 'bg-blue-50 text-blue-600'
              : 'text-gray-700 hover:bg-gray-100',
          ]"
        >
          <span class="text-xl">📋</span>
          Hardware List
        </button>
        <button
          @click="$emit('navigate', 'rentals')"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
            active === 'rentals'
              ? 'bg-blue-50 text-blue-600'
              : 'text-gray-700 hover:bg-gray-100',
          ]"
        >
          <span class="text-xl">🛒</span>
          My Rentals
        </button>
      </div>

      <!-- Admin Section (Only for Admins) -->
      <div v-if="isAdmin" class="border-t border-gray-200 pt-4">
        <p class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">Admin</p>
        <button
          @click="$emit('navigate', 'admin-devices')"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
            active === 'admin-devices'
              ? 'bg-blue-50 text-blue-600'
              : 'text-gray-700 hover:bg-gray-100',
          ]"
        >
          <span class="text-xl">⚙️</span>
          Device Management
        </button>
        <button
          @click="$emit('navigate', 'admin-users')"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
            active === 'admin-users'
              ? 'bg-blue-50 text-blue-600'
              : 'text-gray-700 hover:bg-gray-100',
          ]"
        >
          <span class="text-xl">👥</span>
          User Management
        </button>
      </div>
    </nav>

    <!-- Bottom Section -->
    <div class="p-4 border-t border-gray-200">
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

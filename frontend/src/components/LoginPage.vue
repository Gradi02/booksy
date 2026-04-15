<script setup>
defineProps({
  username: String,
  password: String,
  loading: Boolean,
  error: String,
});

defineEmits(["update:username", "update:password", "login"]);
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex w-16 h-16 bg-white rounded-lg items-center justify-center text-3xl mb-4">
          🔧
        </div>
        <h1 class="text-3xl font-bold text-white">Hardware Manager</h1>
        <p class="text-blue-100 mt-2">Booksy Inventory System</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white rounded-lg shadow-xl p-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Welcome Back</h2>

        <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {{ error }}
        </div>

        <form @submit.prevent="$emit('login')" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              :value="username"
              @input="$emit('update:username', $event.target.value)"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              :value="password"
              @input="$emit('update:password', $event.target.value)"
              type="password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary py-2 text-lg font-semibold"
          >
            {{ loading ? "Signing in..." : "Sign In" }}
          </button>
        </form>

        <div class="mt-6 pt-6 border-t border-gray-200">
          <p class="text-sm text-gray-600 text-center">
            Demo credentials<br />
            <span class="font-medium">admin / admin123</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

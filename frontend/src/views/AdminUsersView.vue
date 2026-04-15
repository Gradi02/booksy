<script setup>
const props = defineProps({
  users: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["add", "edit", "delete"]);

function handleAdd() {
  emit("add");
}

function handleEdit(user) {
  emit("edit", user);
}

function handleDelete(userId) {
  emit("delete", userId);
}
</script>

<template>
  <div>
    <!-- Title & Actions -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
      <h2 class="text-2xl font-bold text-gray-800">User Management</h2>
      <button @click="handleAdd" class="btn-primary">+ Add User</button>
    </div>

    <!-- No Users Message -->
    <div v-if="users.length === 0" class="card p-8 text-center">
      <p class="text-gray-500 text-lg">No users</p>
    </div>

    <!-- Users Table -->
    <div v-else class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Username</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Role</th>
              <th class="px-6 py-3 text-right text-sm font-semibold text-gray-900">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ user.username }}</td>
              <td class="px-6 py-4">
                <span :class="['px-3 py-1 rounded-full text-sm font-medium', user.is_admin ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800']">
                  {{ user.is_admin ? "Admin" : "User" }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex gap-2 justify-end">
                  <button
                    @click="handleEdit(user)"
                    class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 transition-colors"
                  >
                    Edit
                  </button>
                  <button
                    @click="handleDelete(user.id)"
                    class="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

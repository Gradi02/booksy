<script setup>
import StatusBadge from "../components/StatusBadge.vue";

const props = defineProps({
  devices: {
    type: Array,
    required: true,
  },
  currentUser: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["return"]);

function handleReturn(id) {
  emit("return", id);
}
</script>

<template>
  <div>
    <!-- Title -->
    <h2 class="text-2xl font-bold text-gray-800 mb-6">My Rentals</h2>

    <!-- No Rentals Message -->
    <div v-if="devices.length === 0" class="card p-8 text-center">
      <p class="text-gray-500 text-lg">You haven't rented any devices yet</p>
    </div>

    <!-- Rentals Table -->
    <div v-else class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Device Name</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Brand</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Date Added</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Rented By</th>
              <th class="px-6 py-3 text-right text-sm font-semibold text-gray-900">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="device in devices" :key="device.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ device.name }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ device.brand || "-" }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">
                {{ device.purchase_date ? new Date(device.purchase_date).toLocaleDateString() : "-" }}
              </td>
              <td class="px-6 py-4">
                <StatusBadge :status="device.status" />
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ device.assigned_to || "-" }}</td>
              <td class="px-6 py-4 text-right">
                <button
                  @click="handleReturn(device.id)"
                  class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
                >
                  Return
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import StatusBadge from "../components/StatusBadge.vue";

const props = defineProps({
  devices: {
    type: Array,
    required: true,
  },
  statusFilter: {
    type: String,
    required: true,
  },
  sortBy: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["update:status-filter", "update:sort-by", "rent"]);

function handleStatusChange(value) {
  emit("update:status-filter", value);
}

function handleSortChange(value) {
  emit("update:sort-by", value);
}

function handleRent(id) {
  emit("rent", id);
}
</script>

<template>
  <div>
    <!-- Filter & Sort Controls -->
    <div class="flex flex-col md:flex-row gap-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Filter by Status</label>
        <select
          :value="statusFilter"
          @change="handleStatusChange($event.target.value)"
          class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="All">All Statuses</option>
          <option value="Available">Available</option>
          <option value="In Use">In Use</option>
          <option value="Repair">In Repair</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
        <select
          :value="sortBy"
          @change="handleSortChange($event.target.value)"
          class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="date">Date Added (Newest)</option>
          <option value="name">Device Name</option>
          <option value="brand">Brand</option>
        </select>
      </div>
    </div>

    <!-- No Devices Message -->
    <div v-if="devices.length === 0" class="card p-8 text-center">
      <p class="text-gray-500 text-lg">No devices available</p>
    </div>

    <!-- Devices Table -->
    <div v-else class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Device Name</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Brand</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Date Added</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
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
              <td class="px-6 py-4 text-right">
                <button
                  v-if="device.status === 'Available'"
                  @click="handleRent(device.id)"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  Rent
                </button>
                <button
                  v-else
                  disabled
                  class="px-4 py-2 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed text-sm font-medium"
                >
                  Rent
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

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

const emit = defineEmits(["update:status-filter", "update:sort-by", "add", "edit", "delete", "mark-repair"]);

function handleStatusChange(value) {
  emit("update:status-filter", value);
}

function handleSortChange(value) {
  emit("update:sort-by", value);
}

function handleAdd() {
  emit("add");
}

function handleEdit(device) {
  emit("edit", device);
}

function handleDelete(id) {
  emit("delete", id);
}

function handleMarkRepair(id) {
  emit("mark-repair", id);
}
</script>

<template>
  <div>
    <!-- Actions -->
    <div class="flex flex-col md:flex-row justify-end items-start md:items-center mb-6 gap-4">
      <button @click="handleAdd" class="btn-primary">+ Add Device</button>
    </div>

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
      <p class="text-gray-500 text-lg">No devices</p>
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
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Assigned To</th>
              <th class="px-6 py-3 text-right text-sm font-semibold text-gray-900">Actions</th>
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
                <div class="flex gap-2 justify-end flex-wrap">
                  <button
                    @click="handleEdit(device)"
                    class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 transition-colors"
                  >
                    Edit
                  </button>
                  <button
                    @click="handleMarkRepair(device.id)"
                    :disabled="device.status === 'Repair'"
                    class="px-3 py-1 bg-yellow-600 text-white rounded text-sm hover:bg-yellow-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    Mark Repair
                  </button>
                  <button
                    @click="handleDelete(device.id)"
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

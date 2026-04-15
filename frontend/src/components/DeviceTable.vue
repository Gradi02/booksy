<script setup>
import StatusBadge from "./StatusBadge.vue";

defineProps({
  devices: Array,
});

defineEmits(["delete", "update-status"]);

const isRentDisabled = (status) => status !== "Available";
</script>

<template>
  <div class="card overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-200">
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Device Name</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Brand</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Date Added</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Assigned To</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr
            v-for="device in devices"
            :key="device.id"
            class="hover:bg-gray-50 transition-colors"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="font-medium text-gray-900">{{ device.name }}</div>
              <div class="text-sm text-gray-500">ID: {{ device.id }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-700">
              {{ device.brand || "-" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-700">
              {{ device.purchase_date || "-" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-700">
              {{ device.assigned_to || "-" }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <StatusBadge :status="device.status" />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex gap-2">
                <button
                  @click="$emit('update-status', device.id, device.status === 'Available' ? 'In Use' : 'Available')"
                  :disabled="device.status === 'Repair'"
                  :class="[
                    'btn-primary inline-flex items-center',
                    device.status === 'Repair' ? 'opacity-50 cursor-not-allowed' : '',
                  ]"
                >
                  {{ device.status === 'Available' ? 'Rent' : 'Return' }}
                </button>
                <button
                  @click="$emit('delete', device.id)"
                  class="btn-danger inline-flex items-center"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="devices.length === 0">
            <td colspan="6" class="px-6 py-8 text-center text-gray-500">
              No devices found. Add one to get started!
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

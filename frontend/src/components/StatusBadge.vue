<script setup>
defineProps({
  status: String,
});

const statusClasses = {
  Available: "badge badge-available",
  "In Use": "badge badge-in-use",
  Repair: "badge badge-repair",
};
</script>

<template>
  <span :class="statusClasses[status] || 'badge badge-available'">
    {{ status }}
  </span>
</template>

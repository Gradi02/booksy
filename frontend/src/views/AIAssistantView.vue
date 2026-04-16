<template>
  <AIChatPanel @apply-filter="handleAIFilter" />
</template>

<script setup>
import AIChatPanel from "../components/AIChatPanel.vue";

// This view serves as the AI Assistant interface
// It can emit filter commands that affect the Hardware List view

const handleAIFilter = (filter) => {
  console.log("AI Filter received:", filter);
  // This can be connected to global state or event bus
};
</script>

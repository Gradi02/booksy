<script setup>
import { ref } from "vue";
import { callLLM, parseResponseForBackendCommand } from "../services/llmProviders.js";

const props = defineProps({
  devices: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["close", "apply-actions"]);

const apiKey = ref("");
const userPrompt = ref("");
const aiResponse = ref("");
const loading = ref(false);
const error = ref("");
const parsedResult = ref({ commands: [], explanation: "", success: false });

// Hardcoded Gemini 2.5 Flash
const MODEL = "gemini-2.5-flash";
const PROVIDER = "gemini";

async function sendRequest() {
  if (!apiKey.value?.trim() || !userPrompt.value?.trim()) {
    error.value = "API key and prompt are required";
    return;
  }

  error.value = "";
  loading.value = true;
  aiResponse.value = "";
  parsedResult.value = { commands: [], explanation: "", success: false };

  try {
    const response = await callLLM(
      { provider: PROVIDER, apiKey: apiKey.value, model: MODEL },
      userPrompt.value
    );

    aiResponse.value = response;
    parsedResult.value = parseResponseForBackendCommand(response);
  } catch (err) {
    error.value = err.message || "Failed to get AI response";
  } finally {
    loading.value = false;
  }
}

function applyActions() {
  if (parsedResult.value.commands && parsedResult.value.commands.length > 0) {
    window.dispatchEvent(
      new CustomEvent("applyAIActions", {
        detail: parsedResult.value.commands,
      })
    );
    emit("apply-actions", parsedResult.value.commands);
    emit("close");
  }
}

function clearResponse() {
  aiResponse.value = "";
  parsedResult.value = { commands: [], explanation: "", success: false };
}
</script>

<template>
  <div class="flex flex-col h-full bg-white">
    <!-- Header -->
    <div class="flex justify-between items-center p-4 border-b border-gray-200">
      <h2 class="text-lg font-semibold text-gray-800">🤖 Smart Assistant</h2>
      <button
        @click="$emit('close')"
        class="text-gray-500 hover:text-gray-700 text-xl font-bold"
      >
        ✕
      </button>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-auto p-4 space-y-4">
      <!-- API Key Input -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Google Gemini API Key
          <span class="text-xs text-green-600">(memory only)</span>
        </label>
        <input
          v-model="apiKey"
          type="password"
          placeholder="Paste your API key"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
        <p class="text-xs text-gray-500 mt-1">🔒 Never stored, never logged</p>
      </div>

      <!-- Prompt Input -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Query
        </label>
        <textarea
          v-model="userPrompt"
          @keyup.ctrl.enter="sendRequest"
          @keyup.meta.enter="sendRequest"
          placeholder="Ask about your devices..."
          rows="3"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none text-sm"
        ></textarea>
        <p class="text-xs text-gray-500 mt-1">Ctrl+Enter to send</p>
      </div>

      <!-- Error -->
      <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded text-red-800 text-sm">
        <strong>Error:</strong> {{ error }}
      </div>

      <!-- Response -->
      <div v-if="aiResponse" class="space-y-2">
        <div class="text-sm font-semibold text-gray-800">Response:</div>
        <div class="p-3 bg-blue-50 border border-blue-200 rounded text-sm text-gray-700 max-h-24 overflow-auto">
          {{ aiResponse }}
        </div>
        
        <!-- Parsed Commands Display -->
        <div v-if="parsedResult.commands && parsedResult.commands.length > 0" class="p-3 bg-green-50 border border-green-200 rounded text-sm space-y-2">
          <div class="font-semibold text-green-800">Detected Actions:</div>
          <div v-for="(cmd, idx) in parsedResult.commands" :key="idx" class="text-green-700 text-xs pl-3 border-l-2 border-green-400">
            <span class="font-medium">{{ cmd.action }}</span>: {{ cmd.description || `${cmd.target} = ${cmd.value}` }}
          </div>
        </div>
        
        <button
          v-if="parsedResult.commands && parsedResult.commands.length > 0"
          @click="applyActions"
          class="w-full px-3 py-2 bg-green-100 text-green-800 rounded hover:bg-green-200 text-sm font-medium transition"
        >
          ✓ Apply Actions
        </button>
      </div>

      <!-- Tips -->
      <div v-if="!aiResponse" class="text-gray-600 text-xs bg-gray-50 p-2 rounded">
        <strong>💡 Try asking:</strong>
        <ul class="mt-1 space-y-0.5">
          <li>• "Show available devices"</li>
          <li>• "Sort by brand"</li>
          <li>• "My rentals"</li>
          <li>• "Devices in repair sorted by date"</li>
        </ul>
      </div>
    </div>

    <!-- Footer -->
    <div class="p-4 border-t border-gray-200 space-y-2">
      <button
        @click="sendRequest"
        :disabled="!apiKey?.trim() || !userPrompt?.trim() || loading"
        class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition text-sm"
      >
        {{ loading ? "Thinking..." : "Send" }}
      </button>
      <button
        @click="clearResponse"
        :disabled="!aiResponse"
        class="w-full px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 disabled:bg-gray-200 disabled:cursor-not-allowed text-sm transition"
      >
        Clear
      </button>
    </div>
  </div>
</template>

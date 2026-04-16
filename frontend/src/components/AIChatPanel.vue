<template>
  <div class="flex-1 overflow-auto p-6">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">🤖 Smart Assistant</h1>
        <p class="text-gray-600 mt-2">
          Query devices using natural language. AI helps manage equipment and understands your device inventory.
        </p>
      </div>

      <!-- Configuration Panel -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <!-- Provider Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Provider
            </label>
            <select
              v-model="selectedProvider"
              @change="onProviderChange"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Provider</option>
              <option value="openai">OpenAI (GPT-4)</option>
              <option value="gemini">Google Gemini</option>
              <option value="grok">xAI Grok</option>
            </select>
          </div>

          <!-- API Key Input (Memory Only) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              API Key
              <span class="text-xs text-green-600">(memory only)</span>
            </label>
            <input
              v-model="apiKey"
              type="password"
              placeholder="Paste your API key here"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p class="text-xs text-gray-500 mt-1">
              🔒 Never stored, never logged
            </p>
          </div>

          <!-- Model Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Model
              <span class="text-xs text-gray-500">(or custom)</span>
            </label>
            <div class="flex gap-2">
              <select
                v-model="modelMode"
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="preset">Preset</option>
                <option value="custom">Custom</option>
              </select>
              <input
                v-if="modelMode === 'custom'"
                v-model="selectedModel"
                type="text"
                placeholder="e.g., gemini-2.5-flash, gpt-4-turbo"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <select
                v-else
                v-model="selectedModel"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option
                  v-for="model in availableModels"
                  :key="model"
                  :value="model"
                >
                  {{ model }}
                </option>
              </select>
            </div>
            <p class="text-xs text-gray-500 mt-1">
              Custom mode: use any model name from your provider
            </p>
          </div>
        </div>

        <!-- Status Info -->
        <div class="bg-blue-50 border border-blue-200 rounded p-3 text-sm text-blue-800">
          <strong>Smart Assistant:</strong> Enter your API key from your chosen provider. Your key stays in memory and
          is never sent to our backend. Requests go directly to the provider's API. Use any model available from your provider.
        </div>
      </div>

      <!-- Chat Interface -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <!-- Prompt Input -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Your Query
          </label>
          <textarea
            v-model="userPrompt"
            @keyup.ctrl.enter="sendRequest"
            @keyup.meta.enter="sendRequest"
            placeholder="Ask AI about your devices... (Ctrl+Enter to send)"
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          ></textarea>
          <p class="text-xs text-gray-500 mt-1">
            💡 Try: "Show me all available devices" or "Sort devices by purchase date"
          </p>
        </div>

        <!-- Send Button -->
        <div class="flex gap-3 mb-6">
          <button
            @click="sendRequest"
            :disabled="!selectedProvider || !apiKey || !userPrompt || loading"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition"
          >
            {{ loading ? "Thinking..." : "Send" }}
          </button>
          <button
            @click="clearResponse"
            :disabled="!aiResponse"
            class="px-6 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 disabled:bg-gray-200 disabled:cursor-not-allowed font-medium transition"
          >
            Clear
          </button>
        </div>

        <!-- Error Message -->
        <div
          v-if="error"
          class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800"
        >
          <strong>Error:</strong> {{ error }}
        </div>

        <!-- Response Display -->
        <div v-if="aiResponse" class="mb-6">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-lg font-semibold text-gray-800">AI Response</h3>
            <button
              @click="applyToFilter"
              v-if="parsedCommand.filter"
              class="text-xs px-3 py-1 bg-green-100 text-green-800 rounded hover:bg-green-200 transition"
            >
              ✓ Apply Filter
            </button>
          </div>
          <div class="bg-gray-50 border border-gray-300 rounded-lg p-4 max-h-96 overflow-auto">
            <p class="text-gray-800 whitespace-pre-wrap">{{ aiResponse }}</p>
          </div>

          <!-- Parsed Commands Info -->
          <div v-if="showParsedCommands" class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded text-sm">
            <strong class="block mb-2">Detected Commands:</strong>
            <div class="space-y-1 text-blue-800">
              <div v-if="parsedCommand.filter">
                📌 Filter: <code class="bg-white px-2 py-1 rounded">{{ parsedCommand.filter }}</code>
              </div>
              <div v-if="parsedCommand.sort">
                🔄 Sort: <code class="bg-white px-2 py-1 rounded">{{ parsedCommand.sort }}</code>
              </div>
              <div v-if="parsedCommand.search">
                🔍 Search: <code class="bg-white px-2 py-1 rounded">{{ parsedCommand.search }}</code>
              </div>
            </div>
          </div>
        </div>

        <!-- Usage Tips -->
        <div v-if="!aiResponse" class="text-gray-600 text-sm">
          <strong>Tips for better results:</strong>
          <ul class="list-disc list-inside mt-2 space-y-1">
            <li>Use natural language: "Which devices are in repair?"</li>
            <li>Ask for filtering: "Show me only available devices"</li>
            <li>Request sorting: "Sort by brand name"</li>
            <li>Combine queries: "Available devices sorted by date"</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { callLLM, parseResponseForBackendCommand, PROVIDER_CONFIG } from "../services/llmProviders";

// State
const selectedProvider = ref("");
const apiKey = ref("");
const selectedModel = ref("");
const modelMode = ref("preset");
const userPrompt = ref("");
const aiResponse = ref("");
const error = ref("");
const loading = ref(false);
const showParsedCommands = ref(false);
const parsedCommand = ref({ filter: null, sort: null, search: null });

// Computed
const availableModels = computed(() => {
  const config = PROVIDER_CONFIG[selectedProvider.value];
  return config?.models || [];
});

// Methods
function onProviderChange() {
  selectedModel.value = availableModels.value[0] || "";
  error.value = "";
}

async function sendRequest() {
  if (!selectedProvider.value || !apiKey.value || !userPrompt.value) {
    error.value = "Please fill in provider, API key, and prompt";
    return;
  }

  loading.value = true;
  error.value = "";
  aiResponse.value = "";

  try {
    const response = await callLLM(
      {
        provider: selectedProvider.value,
        apiKey: apiKey.value,
        model: selectedModel.value,
      },
      userPrompt.value
    );

    aiResponse.value = response;

    // Parse response for backend commands
    parsedCommand.value = parseResponseForBackendCommand(response);
    showParsedCommands.value = true;
  } catch (err) {
    error.value =
      err.message ||
      "Failed to get response. Check your API key and try again.";
    console.error("LLM Error:", err); // Safe to log error, not the key
  } finally {
    loading.value = false;
  }
}

function clearResponse() {
  aiResponse.value = "";
  error.value = "";
  parsedCommand.value = { filter: null, sort: null, search: null };
  showParsedCommands.value = false;
}

function applyToFilter() {
  // Emit event to parent or update global state
  // This will be connected to the main app filtering
  console.log("Applying filter:", parsedCommand.value);
  
  // Dispatch custom event for parent component to listen
  window.dispatchEvent(
    new CustomEvent("applyAIFilter", {
      detail: parsedCommand.value,
    })
  );

  alert(
    `Filter applied: ${parsedCommand.value.filter || "none"}. Check your Hardware List!`
  );
}
</script>

<style scoped>
textarea:focus {
  outline: none;
}
</style>

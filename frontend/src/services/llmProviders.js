/**
 * LLM Provider Abstraction Layer
 * Unified interface for OpenAI, Gemini, and Grok
 * All API calls use user-provided keys (no backend proxy)
 */

const PROVIDERS = {
  OPENAI: "openai",
  GEMINI: "gemini",
  GROK: "grok",
};

const DEFAULT_MODELS = {
  openai: "gpt-4-turbo",
  gemini: "gemini-pro",
  grok: "grok-1",
};

/**
 * Unified LLM call interface
 * @param {Object} config - { provider, apiKey, model }
 * @param {string} prompt - User's prompt text
 * @returns {Promise<string>} - Normalized text response
 */
export async function callLLM(config, prompt) {
  const { provider, apiKey, model } = config;

  if (!provider || !apiKey) {
    throw new Error("Provider and API key are required");
  }

  const normalizedProvider = provider.toLowerCase();

  switch (normalizedProvider) {
    case PROVIDERS.OPENAI:
      return callOpenAI(apiKey, model || DEFAULT_MODELS.openai, prompt);
    case PROVIDERS.GEMINI:
      return callGemini(apiKey, model || DEFAULT_MODELS.gemini, prompt);
    case PROVIDERS.GROK:
      return callGrok(apiKey, model || DEFAULT_MODELS.grok, prompt);
    default:
      throw new Error(`Unsupported provider: ${provider}`);
  }
}

/**
 * OpenAI API integration
 * Uses chat/completions endpoint
 */
async function callOpenAI(apiKey, model, prompt) {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: "user",
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      error.error?.message || `OpenAI API error: ${response.status}`
    );
  }

  const data = await response.json();
  return data.choices[0]?.message?.content || "";
}

/**
 * Google Gemini API integration
 * Uses generateContent endpoint with different format
 */
async function callGemini(apiKey, model, prompt) {
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      contents: [
        {
          parts: [
            {
              text: prompt,
            },
          ],
        },
      ],
      safetySettings: [
        {
          category: "HARM_CATEGORY_HATE_SPEECH",
          threshold: "BLOCK_NONE",
        },
        {
          category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          threshold: "BLOCK_NONE",
        },
        {
          category: "HARM_CATEGORY_DANGEROUS_CONTENT",
          threshold: "BLOCK_NONE",
        },
        {
          category: "HARM_CATEGORY_HARASSMENT",
          threshold: "BLOCK_NONE",
        },
      ],
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 2000,
      },
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      error.error?.message || `Gemini API error: ${response.status}`
    );
  }

  const data = await response.json();
  return (
    data.candidates?.[0]?.content?.parts?.[0]?.text ||
    "No response generated"
  );
}

/**
 * Grok API integration (xAI)
 * Uses OpenAI-compatible chat/completions format
 */
async function callGrok(apiKey, model, prompt) {
  const response = await fetch("https://api.x.ai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: model || "grok-1",
      messages: [
        {
          role: "user",
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Grok API error: ${error.error?.message || response.status}`);
  }

  const data = await response.json();
  return data.choices[0]?.message?.content || "";
}

/**
 * Utility: Parse LLM response for backend filtering/sorting commands
 * Returns structured commands that can be executed as actions
 * @param {string} response - LLM response text
 * @returns {Object} - Parsed commands { commands: [], explanation }
 */
export function parseResponseForBackendCommand(response) {
  // Parse response and extract multiple commands
  // This maps AI understanding to actionable frontend commands
  
  const lowercaseResponse = response.toLowerCase();
  const commands = [];
  let explanation = response;
  
  // FILTER ACTIONS
  if (lowercaseResponse.includes("available")) {
    commands.push({
      action: "filter",
      target: "status",
      value: "Available",
      description: "Show available devices"
    });
  } else if (lowercaseResponse.includes("in use") || lowercaseResponse.includes("in-use")) {
    commands.push({
      action: "filter",
      target: "status",
      value: "In Use",
      description: "Show devices in use"
    });
  } else if (lowercaseResponse.includes("repair") || lowercaseResponse.includes("broken")) {
    commands.push({
      action: "filter",
      target: "status",
      value: "Repair",
      description: "Show devices in repair"
    });
  } else if (lowercaseResponse.includes("all devices") || lowercaseResponse.includes("show all")) {
    commands.push({
      action: "filter",
      target: "status",
      value: "All",
      description: "Show all devices"
    });
  }
  
  // SORT ACTIONS
  if (lowercaseResponse.includes("sort by brand") || lowercaseResponse.includes("by brand")) {
    commands.push({
      action: "sort",
      target: "sort_by",
      value: "brand",
      description: "Sort by brand"
    });
  } else if (lowercaseResponse.includes("sort by date") || lowercaseResponse.includes("newest") || lowercaseResponse.includes("oldest")) {
    commands.push({
      action: "sort",
      target: "sort_by",
      value: "date",
      description: "Sort by date"
    });
  } else if (lowercaseResponse.includes("sort by name") || lowercaseResponse.includes("alphabetically")) {
    commands.push({
      action: "sort",
      target: "sort_by",
      value: "name",
      description: "Sort by name"
    });
  }
  
  // SEARCH ACTIONS
  const searchMatch = response.match(/"([^"]+)"/);
  if (searchMatch) {
    commands.push({
      action: "search",
      target: "search",
      value: searchMatch[1],
      description: `Search for '${searchMatch[1]}'`
    });
  }
  
  // NAVIGATION ACTIONS
  if (lowercaseResponse.includes("rental") || lowercaseResponse.includes("my rental") || lowercaseResponse.includes("renting")) {
    commands.push({
      action: "navigate",
      target: "view",
      value: "rentals",
      description: "Go to my rentals"
    });
  } else if (lowercaseResponse.includes("admin") || lowercaseResponse.includes("manage device") || lowercaseResponse.includes("management")) {
    commands.push({
      action: "navigate",
      target: "view",
      value: "admin-devices",
      description: "Go to device management"
    });
  }
  
  return {
    commands,
    explanation,
    success: commands.length > 0
  };
}

/**
 * Provider configuration
 */
export const PROVIDER_CONFIG = {
  [PROVIDERS.OPENAI]: {
    name: "OpenAI",
    models: [
      "gpt-4-turbo",
      "gpt-4",
      "gpt-4o",
      "gpt-4o-mini",
      "gpt-3.5-turbo",
    ],
    docUrl: "https://platform.openai.com/docs/guides/gpt",
  },
  [PROVIDERS.GEMINI]: {
    name: "Google Gemini",
    models: [
      "gemini-pro",
      "gemini-1.5-pro",
      "gemini-1.5-flash",
      "gemini-2.0-flash",
      "gemini-2.5-flash",
      "gemini-2.5-pro",
    ],
    docUrl: "https://ai.google.dev/docs",
  },
  [PROVIDERS.GROK]: {
    name: "xAI Grok",
    models: ["grok-1", "grok-vision-beta", "grok-2"],
    docUrl: "https://docs.x.ai",
  },
};

export { PROVIDERS };

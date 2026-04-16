# Smart Assistant Integration Guide

## Overview

The Booksy Hardware Manager now includes a **Smart Assistant** - an AI-powered equipment management tool that helps you discover, filter, and understand your device inventory using natural language. This feature supports multiple AI providers with user-provided API keys.

## Features

### ✅ Supported Providers
- **OpenAI** (GPT-4, GPT-4o, GPT-3.5 Turbo, and more)
- **Google Gemini** (Gemini Pro, Gemini 1.5, **Gemini 2.5** ✨)
- **xAI Grok** (Grok-1, **Grok-2** ✨)

### ✅ Security
- **No developer keys stored** - All requests use user-provided API keys
- **In-memory only** - API keys never persisted to disk or localStorage
- **Never logged** - Safe to use without key exposure
- **Direct API calls** - No backend proxy needed

### ✅ Functionality
- Natural language device queries
- Automatic response parsing for filter/sort commands
- One-click filter application to Hardware List
- Error handling with user-friendly messages

---

## How to Use

### Step 1: Navigate to Smart Assistant
Click the **🤖 Smart Assistant** button in the sidebar (available to all users)

### Step 2: Select Provider
Choose from OpenAI, Gemini, or Grok in the dropdown

### Step 3: Enter Your API Key
- Paste your API key from the chosen provider
- Key stays in memory only (never stored or logged)
- You can switch providers/keys without losing history

### Step 4: Choose Model
**Two modes available:**

**Preset Mode (Recommended for beginners):**
- Dropdown with curated, tested models for each provider
- Safe defaults that work well

**Custom Mode (For power users):**
- Toggle to "Custom"
- Type any model name directly
- Examples: `gemini-2.5-flash`, `gpt-4o-mini`, `grok-2`, `claude-3-opus`
- Allows you to access latest models immediately without code updates

### Step 5: Write Your Query
Examples:
```
"Show me all available devices"
"Which devices are in repair?"
"Sort devices by brand"
"Find Apple devices in use"
```

### Step 6: Send Request
- Click **Send** or press `Ctrl+Enter`
- AI processes your query and returns results

### Step 7: Apply Results (Optional)
If the AI detected filter commands:
- Click **✓ Apply Filter** to update Hardware List
- Auto-switches to Hardware List with filters applied

---

## Model Support

### OpenAI Models
**Preset:**
- gpt-4-turbo (default)
- gpt-4
- gpt-4o
- gpt-4o-mini
- gpt-3.5-turbo

**Custom:** Any OpenAI model (e.g., `gpt-4-turbo-preview`, `gpt-4-vision-preview`)

### Google Gemini Models
**Preset:**
- gemini-pro (default)
- gemini-1.5-pro
- gemini-1.5-flash
- gemini-2.0-flash
- gemini-2.5-flash ✨ **NEW**
- gemini-2.5-pro ✨ **NEW**

**Custom:** Any Gemini model (e.g., `gemini-experimental`)

### xAI Grok Models
**Preset:**
- grok-1 (default)
- grok-vision-beta
- grok-2 ✨ **NEW**

**Custom:** Any Grok model (e.g., `grok-2-vision-preview`)

---

### OpenAI
1. Go to https://platform.openai.com/api/keys
2. Create a new API key
3. Cost: Pay-as-you-go (GPT-4 Turbo: ~$0.01-0.03 per query)

### Google Gemini
1. Go to https://aistudio.google.com/app/apikey
2. Create API key for free tier
3. Cost: Free tier limited to 60 requests/minute

### xAI Grok
1. Go to https://docs.x.ai (requires account)
2. Create API key in console
3. Cost: TBD (early access)

---

## Example Queries & Results

### Query 1: Filter by Status
```
User: "Show me available devices"
AI Response: "Here are the available devices: ..."
Detected Command: Filter = "Available"
Result: Hardware List filters to show only Available items
```

### Query 2: Sort Request
```
User: "Sort devices by purchase date, newest first"
AI Response: "Devices sorted by date: ..."
Detected Command: Sort = "date"
Result: Hardware List reorders items by date
```

### Query 3: Complex Query
```
User: "What Apple devices are currently in repair?"
AI Response: "Based on your inventory: MacBook Pro (in repair), iPad Pro (in repair)"
Result: Can manually apply filter or just read response
```

---

## Technical Details

### Architecture
- **Frontend-only** - No backend processing needed
- **Provider abstraction layer** - `llmProviders.js` handles all APIs
- **Unified interface** - Same `callLLM()` function for all providers
- **Response normalization** - All responses converted to plain text
- **Command parsing** - Automatic extraction of filter/sort intents

### File Structure
```
frontend/
├── src/
│   ├── services/
│   │   └── llmProviders.js          # Provider adapters & callLLM()
│   ├── components/
│   │   └── AIChatPanel.vue          # UI component
│   └── views/
│       └── AIAssistantView.vue      # AI view
├── App.vue                           # Added AI filter listener
└── Sidebar.vue                       # Added AI navigation
```

### Supported Commands (Parsed from AI Response)
- **Filter**: "Available", "In Use", "Repair"
- **Sort**: "date", "brand", "name"
- **Search**: Text between quotes in response

---

## Error Handling

### Invalid API Key
```
Error: "invalid_api_key" or "Unauthorized"
Action: Check key is correct from provider dashboard
```

### Rate Limit Exceeded
```
Error: "Rate limit exceeded"
Action: Wait a moment and retry
```

### Network Error
```
Error: "Failed to connect to provider"
Action: Check internet connection
```

### Unsupported Model
```
Error: "Model not found"
Action: Select a different model from dropdown
```

---

## Privacy & Security Notes

1. **API keys are NEVER stored**
   - Only held in memory during the session
   - Cleared when you close the browser/app
   - Not saved to localStorage

2. **No logging**
   - API keys never appear in console logs
   - Requests go directly to provider (no proxy)
   - Your data stays between you and the AI provider

3. **Responsibility**
   - Keep your API keys private
   - You're responsible for API costs
   - Be mindful of rate limits per provider

4. **Provider Terms**
   - Using OpenAI: Subject to OpenAI Terms
   - Using Gemini: Subject to Google Terms
   - Using Grok: Subject to xAI Terms

---

## Future Enhancements

- [ ] Add Claude API support (Anthropic)
- [ ] Implement conversation history
- [ ] Add streaming responses
- [ ] Support for voice input/output
- [ ] Backend integration for advanced filtering
- [ ] Caching of similar queries
- [ ] Custom provider support

---

## Troubleshooting

### "API key not working"
- Double-check the key was copied completely
- Verify it's from the correct provider
- Check if key has expired or been revoked
- Ensure key has necessary permissions

### "No response received"
- Check internet connection
- Try a simpler query
- Switch to different provider to test
- Check if provider API is operational

### "Wrong filters applied"
- AI may not have understood query perfectly
- Try rephrasing: "Show only available devices"
- Manually adjust filters in Hardware List
- Consider using more specific terms

---

## Code Examples

### Using `callLLM()` in your own code
```javascript
import { callLLM, parseResponseForBackendCommand } from '@/services/llmProviders';

const response = await callLLM({
  provider: 'openai',
  apiKey: userProvidedKey,
  model: 'gpt-4-turbo'
}, 'Show me available devices');

const commands = parseResponseForBackendCommand(response);
console.log(commands.filter); // "Available"
```

### Adding a new provider
```javascript
// Add to llmProviders.js
async function callNewProvider(apiKey, model, prompt) {
  // Implement provider-specific API call
  // Return normalized text response
  return normalizedResponse;
}

// Update callLLM()
case 'new-provider':
  return callNewProvider(apiKey, model, prompt);
```

---

## Support

For issues:
1. Check this documentation first
2. Verify your API key with the provider's test endpoint
3. Try with a different provider to isolate issues
4. Check browser console for error details (API key won't be logged)


<script setup>
import { ref, computed, onMounted } from "vue";
import Sidebar from "./components/Sidebar.vue";
import Header from "./components/Header.vue";
import LoginPage from "./components/LoginPage.vue";
import HardwareListView from "./views/HardwareListView.vue";
import MyRentalsView from "./views/MyRentalsView.vue";
import AdminDevicesView from "./views/AdminDevicesView.vue";
import AdminUsersView from "./views/AdminUsersView.vue";
import AIChatModal from "./components/AIChatModal.vue";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// Authentication & User State
const username = ref("admin@booksy.com");
const password = ref("admin");
const token = ref("");
const currentUser = ref(null);
const error = ref("");
const loading = ref(false);
const searchQuery = ref("");
const currentView = ref("hardware");

// Data state
const devices = ref([]);
const users = ref([]);

// AI Panel state
const showAIPanel = ref(false);

// Modal states
const showDeviceModal = ref(false);
const showUserModal = ref(false);
const editingDevice = ref(null);
const editingUser = ref(null);

// Filter & Sort state
const statusFilter = ref("All");
const sortBy = ref("date");

const newDevice = ref({
  name: "",
  brand: "",
  purchase_date: "",
  status: "Available",
  notes: "",
});

const newUser = ref({
  username: "",
  password: "",
  is_admin: false,
});

// Session persistence
function saveSession() {
  if (token.value && currentUser.value) {
    localStorage.setItem("token", token.value);
    localStorage.setItem("currentUser", JSON.stringify(currentUser.value));
  }
}

function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("currentUser");
}

function restoreSession() {
  const savedToken = localStorage.getItem("token");
  const savedUser = localStorage.getItem("currentUser");
  if (savedToken && savedUser) {
    token.value = savedToken;
    currentUser.value = JSON.parse(savedUser);
    
    // Verify admin status with backend (in case it changed)
    fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token.value}` },
    })
      .then(res => res.ok ? res.json() : null)
      .then(userData => {
        if (userData) {
          currentUser.value = userData;
        }
      })
      .catch(() => {
        // If verification fails, clear session
        clearSession();
      });
    
    // Reload data after restoring session
    Promise.all([fetchDevices(), fetchUsers()]);
  }
}

onMounted(() => {
  restoreSession();
  setupAIFilterListener();
});

// Setup listener for AI actions from AIChatModal
function setupAIFilterListener() {
  window.addEventListener("applyAIActions", (event) => {
    const commands = event.detail;
    if (!Array.isArray(commands)) return;
    
    commands.forEach(cmd => {
      switch (cmd.action) {
        case "filter":
          if (cmd.target === "status") {
            statusFilter.value = cmd.value;
          }
          break;
        
        case "sort":
          if (cmd.target === "sort_by") {
            sortBy.value = cmd.value;
          }
          break;
        
        case "search":
          if (cmd.target === "search") {
            searchQuery.value = cmd.value;
          }
          break;
        
        case "navigate":
          if (cmd.target === "view") {
            navigateTo(cmd.value);
          }
          break;
        
        case "click":
          // Handle button clicks if needed
          if (cmd.target === "rent" && cmd.value) {
            rentDevice(parseInt(cmd.value));
          } else if (cmd.target === "return" && cmd.value) {
            returnDevice(parseInt(cmd.value));
          }
          break;
      }
    });
    
    // Switch to hardware or appropriate view if filtering
    if (commands.some(c => c.action === "filter" || c.action === "sort" || c.action === "search")) {
      if (currentView.value !== "admin-devices" && currentView.value !== "admin-users") {
        currentView.value = "hardware";
      }
    }
  });
}

// Centralized API call handler with auto-logout on 401
async function apiCall(url, options = {}) {
  const headers = options.headers || {};
  headers.Authorization = `Bearer ${token.value}`;
  
  try {
    const response = await fetch(url, { ...options, headers });
    
    // Auto-logout on 401 (token expired/invalid)
    if (response.status === 401) {
      error.value = "Session expired. Please login again.";
      logout();
      return null;
    }
    
    return response;
  } catch (err) {
    throw err;
  }
}

// Computed properties for filtering
const filteredDevices = computed(() => {
  let filtered = devices.value;
  
  if (statusFilter.value !== "All") {
    filtered = filtered.filter(d => d.status === statusFilter.value);
  }
  
  const sorted = [...filtered];
  if (sortBy.value === "date") {
    sorted.sort((a, b) => new Date(b.purchase_date || 0) - new Date(a.purchase_date || 0));
  } else if (sortBy.value === "name") {
    sorted.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sortBy.value === "brand") {
    sorted.sort((a, b) => (a.brand || "").localeCompare(b.brand || ""));
  }
  
  return sorted;
});

const myRentals = computed(() => {
  return devices.value.filter(d => d.assigned_to === currentUser.value?.username);
});

// API Functions
async function login() {
  error.value = "";
  loading.value = true;
  try {
    const body = new URLSearchParams();
    body.append("username", username.value);
    body.append("password", password.value);
    const response = await fetch(`${API_BASE}/auth/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    if (!response.ok) throw new Error("Invalid credentials");
    const data = await response.json();
    token.value = data.access_token;
    
    // Fetch actual user info from backend to get correct admin status
    const userResponse = await fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token.value}` },
    });
    if (userResponse.ok) {
      const userData = await userResponse.json();
      currentUser.value = userData;
    } else {
      // Fallback if /auth/me fails
      currentUser.value = {
        username: username.value,
        is_admin: false,
      };
    }
    
    saveSession();
    await Promise.all([fetchDevices(), fetchUsers()]);
  } catch (err) {
    error.value = err.message || "Login failed";
  } finally {
    loading.value = false;
  }
}

async function logout() {
  token.value = "";
  currentUser.value = null;
  devices.value = [];
  users.value = [];
  error.value = "";
  currentView.value = "hardware";
  clearSession();
}

async function fetchDevices() {
  if (!token.value) return;
  try {
    const response = await apiCall(`${API_BASE}/devices`);
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to load devices");
    devices.value = await response.json();
  } catch (err) {
    error.value = err.message || "Failed to fetch devices";
  }
}

async function fetchUsers() {
  if (!token.value || !currentUser.value?.is_admin) return;
  try {
    const response = await apiCall(`${API_BASE}/users`);
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to load users");
    users.value = await response.json();
  } catch (err) {
    // Silently fail if endpoint doesn't exist
  }
}

// Device Management
async function addDevice() {
  error.value = "";
  if (!newDevice.value.name || !newDevice.value.name.trim()) {
    error.value = "Device name is required";
    return;
  }
  try {
    const response = await apiCall(`${API_BASE}/devices`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newDevice.value),
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to create device");
    await fetchDevices();
    showDeviceModal.value = false;
    resetDeviceForm();
  } catch (err) {
    error.value = err.message || "Failed to create device";
  }
}

async function updateDevice() {
  if (!editingDevice.value?.id) return;
  error.value = "";
  if (!newDevice.value.name || !newDevice.value.name.trim()) {
    error.value = "Device name is required";
    return;
  }
  try {
    const response = await apiCall(`${API_BASE}/devices/${editingDevice.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newDevice.value),
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to update device");
    await fetchDevices();
    showDeviceModal.value = false;
    resetDeviceForm();
  } catch (err) {
    error.value = err.message || "Failed to update device";
  }
}

async function deleteDevice(id) {
  if (!confirm("Are you sure you want to delete this device?")) return;
  error.value = "";
  try {
    const response = await apiCall(`${API_BASE}/devices/${id}`, {
      method: "DELETE",
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to delete device");
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Failed to delete device";
  }
}

async function updateDeviceStatus(id, status) {
  error.value = "";
  try {
    const response = await apiCall(`${API_BASE}/devices/${id}/status/${status}`, {
      method: "PATCH",
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to update status");
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Failed to update device status";
  }
}

// Rental Actions
async function rentDevice(id) {
  error.value = "";
  try {
    const device = devices.value.find(d => d.id === id);
    if (!device) throw new Error("Device not found");
    
    const updateData = {
      ...device,
      status: "In Use",
      assigned_to: currentUser.value.username,
    };
    
    const response = await apiCall(`${API_BASE}/devices/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to rent device");
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Failed to rent device";
  }
}

async function returnDevice(id) {
  error.value = "";
  try {
    const device = devices.value.find(d => d.id === id);
    if (!device) throw new Error("Device not found");
    
    const updateData = {
      ...device,
      status: "Available",
      assigned_to: null,
    };
    
    const response = await apiCall(`${API_BASE}/devices/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) throw new Error("Failed to return device");
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Failed to return device";
  }
}

async function markInRepair(id) {
  await updateDeviceStatus(id, "Repair");
}

// User Management
async function addUser() {
  error.value = "";
  try {
    const response = await apiCall(`${API_BASE}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newUser.value),
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || "Failed to create user");
    }
    await fetchUsers();
    showUserModal.value = false;
    resetUserForm();
  } catch (err) {
    error.value = err.message || "Failed to create user";
  }
}

async function updateUser() {
  if (!editingUser.value?.id) return;
  error.value = "";
  try {
    const response = await apiCall(`${API_BASE}/users/${editingUser.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newUser.value),
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || "Failed to update user");
    }
    await fetchUsers();
    showUserModal.value = false;
    resetUserForm();
  } catch (err) {
    error.value = err.message || "Failed to update user";
  }
}

async function deleteUser(id) {
  // Prevent user from deleting themselves
  const userToDelete = users.value.find(u => u.id === id);
  if (userToDelete && userToDelete.username === currentUser.value.username) {
    error.value = "You cannot delete your own account";
    return;
  }
  
  if (!confirm("Are you sure you want to delete this user?")) return;
  error.value = "";
  try {
    const response = await apiCall(`${API_BASE}/users/${id}`, {
      method: "DELETE",
    });
    if (!response) return; // Auto-logout happened
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || "Failed to delete user");
    }
    await fetchUsers();
  } catch (err) {
    error.value = err.message || "Failed to delete user";
  }
}

// Modal Handlers
function openDeviceModal(device = null) {
  if (device) {
    editingDevice.value = device;
    newDevice.value = { ...device };
  } else {
    editingDevice.value = null;
    resetDeviceForm();
  }
  showDeviceModal.value = true;
}

function closeDeviceModal() {
  showDeviceModal.value = false;
  editingDevice.value = null;
  resetDeviceForm();
}

function resetDeviceForm() {
  newDevice.value = {
    name: "",
    brand: "",
    purchase_date: null,
    status: "Available",
    notes: "",
  };
}

function openUserModal(user = null) {
  if (user) {
    editingUser.value = user;
    newUser.value = { username: user.username, password: "", is_admin: user.is_admin };
  } else {
    editingUser.value = null;
    resetUserForm();
  }
  showUserModal.value = true;
}

function closeUserModal() {
  showUserModal.value = false;
  editingUser.value = null;
  resetUserForm();
}

function resetUserForm() {
  newUser.value = {
    username: "",
    password: "",
    is_admin: false,
  };
}

// View Navigation
function navigateTo(view) {
  if (view === "admin-devices" || view === "admin-users") {
    if (!currentUser.value?.is_admin) {
      error.value = "Admin access required";
      return;
    }
  }
  currentView.value = view;
  error.value = "";
}

</script>

<template>
  <div v-if="!token">
    <LoginPage
      v-model:username="username"
      v-model:password="password"
      :loading="loading"
      :error="error"
      @login="login"
    />
  </div>

  <div v-else class="flex h-screen bg-gray-100">
    <Sidebar 
      :active="currentView" 
      :is-admin="currentUser?.is_admin"
      @navigate="navigateTo"
      @logout="logout" 
    />

    <div class="flex-1 flex flex-col overflow-hidden">
      <Header
        :current-view="currentView"
      />

      <main class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto">
          <!-- Error Message -->
          <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {{ error }}
          </div>

          <!-- Hardware List View -->
          <HardwareListView
            v-if="currentView === 'hardware'"
            :devices="filteredDevices"
            :status-filter="statusFilter"
            :sort-by="sortBy"
            @update:status-filter="statusFilter = $event"
            @update:sort-by="sortBy = $event"
            @rent="rentDevice"
          />

          <!-- My Rentals View -->
          <MyRentalsView
            v-if="currentView === 'rentals'"
            :devices="myRentals"
            :current-user="currentUser"
            @return="returnDevice"
          />

          <!-- Admin Devices View -->
          <AdminDevicesView
            v-if="currentView === 'admin-devices' && currentUser?.is_admin"
            :devices="filteredDevices"
            :status-filter="statusFilter"
            :sort-by="sortBy"
            @update:status-filter="statusFilter = $event"
            @update:sort-by="sortBy = $event"
            @add="openDeviceModal()"
            @edit="openDeviceModal"
            @delete="deleteDevice"
            @mark-repair="markInRepair"
          />

          <!-- Admin Users View -->
          <AdminUsersView
            v-if="currentView === 'admin-users' && currentUser?.is_admin"
            :users="users"
            @add="openUserModal()"
            @edit="openUserModal"
            @delete="deleteUser"
          />
        </div>
      </main>

      <!-- Floating AI Chat Button (Right bottom corner) -->
      <button
        @click="showAIPanel = !showAIPanel"
        class="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 flex items-center justify-center text-2xl transition-all hover:scale-110 z-40"
        title="Smart Assistant"
      >
        🤖
      </button>

      <!-- AI Chat Modal (Right side panel) -->
      <div
        v-if="showAIPanel"
        class="fixed bottom-24 right-6 w-80 h-96 bg-white rounded-lg shadow-2xl border border-gray-200 z-40 flex flex-col"
      >
        <AIChatModal
          :devices="devices"
          @close="showAIPanel = false"
        />
      </div>
    </div>

    <!-- Device Modal -->
    <div v-if="showDeviceModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="card p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold mb-4">
          {{ editingDevice ? "Edit Device" : "Add New Device" }}
        </h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Device Name *</label>
            <input
              v-model="newDevice.name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Brand</label>
            <input
              v-model="newDevice.brand"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Purchase Date</label>
            <input
              v-model="newDevice.purchase_date"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              v-model="newDevice.status"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="Available">Available</option>
              <option value="In Use">In Use</option>
              <option value="Repair">Repair</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
            <input
              v-model="newDevice.notes"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
        <div class="flex gap-3 mt-6">
          <button 
            @click="editingDevice ? updateDevice() : addDevice()" 
            class="btn-primary flex-1"
            :disabled="!newDevice.name?.trim()"
          >
            {{ editingDevice ? "Save" : "Create" }}
          </button>
          <button @click="closeDeviceModal" class="btn-secondary flex-1">Cancel</button>
        </div>
      </div>
    </div>

    <!-- User Modal -->
    <div v-if="showUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="card p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold mb-4">
          {{ editingUser ? "Edit User" : "Add New User" }}
        </h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email/Username *</label>
            <input
              v-model="newUser.username"
              type="email"
              :disabled="!!editingUser"
              placeholder="user@booksy.com"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
              required
            />
            <p class="text-xs text-gray-500 mt-1">Must end with @booksy.com</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ editingUser ? "New Password (leave blank to keep)" : "Password *" }}
            </label>
            <input
              v-model="newUser.password"
              type="password"
              placeholder="At least 8 characters"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              :required="!editingUser"
            />
            <p class="text-xs text-gray-500 mt-1">Minimum 8 characters</p>
          </div>
          <div class="flex items-center">
            <input
              v-model="newUser.is_admin"
              type="checkbox"
              id="is_admin"
              :disabled="!!editingUser"
              class="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            />
            <label for="is_admin" class="ml-2 text-sm font-medium text-gray-700">
              Admin Role
              <span v-if="editingUser" class="text-xs text-gray-500">(cannot change for existing users)</span>
            </label>
          </div>
        </div>
        <div class="flex gap-3 mt-6">
          <button 
            @click="editingUser ? updateUser() : addUser()" 
            class="btn-primary flex-1"
            :disabled="!newUser.username?.trim() || (!editingUser && !newUser.password?.trim())"
          >
            {{ editingUser ? "Save" : "Create" }}
          </button>
          <button @click="closeUserModal" class="btn-secondary flex-1">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>


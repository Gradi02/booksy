<script setup>
import { ref, computed } from "vue";
import Sidebar from "./components/Sidebar.vue";
import Header from "./components/Header.vue";
import LoginPage from "./components/LoginPage.vue";
import HardwareListView from "./views/HardwareListView.vue";
import MyRentalsView from "./views/MyRentalsView.vue";
import AdminDevicesView from "./views/AdminDevicesView.vue";
import AdminUsersView from "./views/AdminUsersView.vue";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// Authentication & User State
const username = ref("admin");
const password = ref("admin123");
const token = ref("");
const currentUser = ref(null); // Will store user info after login
const error = ref("");
const loading = ref(false);
const searchQuery = ref("");
const currentView = ref("hardware"); // hardware, rentals, admin-devices, admin-users

// Data state
const devices = ref([]);
const users = ref([]);

// Modal states
const showDeviceModal = ref(false);
const showUserModal = ref(false);
const editingDevice = ref(null);
const editingUser = ref(null);

// Filter & Sort state
const statusFilter = ref("All");
const sortBy = ref("date"); // date, name, brand

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
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Login failed";
  } finally {
    loading.value = false;
  }
}

async function logout() {
  token.value = "";
  devices.value = [];
  error.value = "";
}

async function fetchDevices() {
  if (!token.value) return;
  error.value = "";
  try {
    const response = await fetch(`${API_BASE}/devices`, {
      headers: { Authorization: `Bearer ${token.value}` },
    });
    if (!response.ok) throw new Error("Failed to load devices");
    devices.value = await response.json();
  } catch (err) {
    error.value = err.message || "Failed to fetch data";
  }
}

async function addDevice() {
  error.value = "";
  try {
    const response = await fetch(`${API_BASE}/devices`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token.value}`,
      },
      body: JSON.stringify(newDevice.value),
    });
    if (!response.ok) throw new Error("Failed to create device");
    await fetchDevices();
    showAddForm.value = false;
    newDevice.value = {
      name: "",
      brand: "",
      purchase_date: "",
      status: "Available",
      notes: "",
      assigned_to: "",
    };
  } catch (err) {
    error.value = err.message || "Failed to create device";
  }
}

async function deleteDevice(id) {
  if (!confirm("Delete this device?")) return;
  error.value = "";
  try {
    const response = await fetch(`${API_BASE}/devices/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token.value}` },
    });
    if (!response.ok) throw new Error("Failed to delete device");
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Failed to delete device";
  }
}

async function updateStatus(id, status) {
  error.value = "";
  try {
    const response = await fetch(`${API_BASE}/devices/${id}/status/${status}`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token.value}` },
    });
    if (!response.ok) throw new Error("Failed to update status");
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Failed to update status";
  }
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
    <Sidebar :active="activeNav" @logout="logout" />

    <div class="flex-1 flex flex-col overflow-hidden">
      <Header
        v-model:search="searchQuery"
        :device-count="filteredDevices.length"
        @refresh="fetchDevices"
      />

      <main class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto">
          <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {{ error }}
          </div>

          <div v-if="!showAddForm" class="mb-6">
            <button @click="showAddForm = true" class="btn-primary">
              + Add Device
            </button>
          </div>

          <div v-if="showAddForm" class="card p-6 mb-6">
            <h3 class="text-lg font-semibold mb-4">Add New Device</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Device Name *
                </label>
                <input
                  v-model="newDevice.name"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Brand
                </label>
                <input
                  v-model="newDevice.brand"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Date
                </label>
                <input
                  v-model="newDevice.purchase_date"
                  type="date"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
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
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Assigned To
                </label>
                <input
                  v-model="newDevice.assigned_to"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Notes
                </label>
                <input
                  v-model="newDevice.notes"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <div class="flex gap-3 mt-4">
              <button @click="addDevice" class="btn-primary">Create Device</button>
              <button @click="showAddForm = false" class="btn-secondary">Cancel</button>
            </div>
          </div>

          <DeviceTable
            :devices="filteredDevices"
            @delete="deleteDevice"
            @update-status="updateStatus"
          />
        </div>
      </main>
    </div>
  </div>
</template>


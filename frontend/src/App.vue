<script setup>
import { ref } from "vue";

const API_BASE = "http://127.0.0.1:8000";

const username = ref("admin");
const password = ref("admin123");
const token = ref("");
const devices = ref([]);
const error = ref("");
const loading = ref(false);
const showAddForm = ref(false);
const newDevice = ref({
  name: "",
  brand: "",
  purchase_date: "",
  status: "Available",
  notes: "",
  assigned_to: "",
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
}

async function fetchDevices() {
  if (!token.value) return;
  error.value = "";
  loading.value = true;
  try {
    const response = await fetch(`${API_BASE}/devices`, {
      headers: { Authorization: `Bearer ${token.value}` },
    });
    if (!response.ok) throw new Error("Failed to load devices");
    devices.value = await response.json();
  } catch (err) {
    error.value = err.message || "Failed to fetch data";
  } finally {
    loading.value = false;
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
    newDevice.value = { name: "", brand: "", purchase_date: "", status: "Available", notes: "", assigned_to: "" };
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
  <div>
    <h1>Booksy Inventory</h1>
    
    <div v-if="!token">
      <h2>Login</h2>
      <div>
        <label>Username: <input v-model="username" type="text" /></label>
      </div>
      <div>
        <label>Password: <input v-model="password" type="password" /></label>
      </div>
      <button @click="login" :disabled="loading">Login</button>
      <p v-if="error">{{ error }}</p>
    </div>

    <div v-if="token">
      <button @click="logout">Logout</button>
      <button @click="fetchDevices" :disabled="loading">Refresh</button>
      <p v-if="error">{{ error }}</p>

      <div v-if="showAddForm">
        <h3>Add Device</h3>
        <div>
          <label>Name: <input v-model="newDevice.name" type="text" required /></label>
        </div>
        <div>
          <label>Brand: <input v-model="newDevice.brand" type="text" /></label>
        </div>
        <div>
          <label>Date: <input v-model="newDevice.purchase_date" type="date" /></label>
        </div>
        <div>
          <label>Assigned To: <input v-model="newDevice.assigned_to" type="text" /></label>
        </div>
        <div>
          <label>Notes: <input v-model="newDevice.notes" type="text" /></label>
        </div>
        <button @click="addDevice">Add</button>
        <button @click="showAddForm = false">Cancel</button>
      </div>
      <button v-else @click="showAddForm = true">Add Device</button>

      <table border="1" cellpadding="5" cellspacing="0" style="margin-top: 20px; border-collapse: collapse;">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Brand</th>
            <th>Date</th>
            <th>Assigned To</th>
            <th>Notes</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="device in devices" :key="device.id">
            <td>{{ device.id }}</td>
            <td>{{ device.name }}</td>
            <td>{{ device.brand || "-" }}</td>
            <td>{{ device.purchase_date || "-" }}</td>
            <td>{{ device.assigned_to || "-" }}</td>
            <td>{{ device.notes || "-" }}</td>
            <td>
              <select :value="device.status" @change="(e) => updateStatus(device.id, e.target.value)">
                <option value="Available">Available</option>
                <option value="In Use">In Use</option>
                <option value="Repair">Repair</option>
              </select>
            </td>
            <td>
              <button @click="deleteDevice(device.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

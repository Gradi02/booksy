<script setup>
import { ref } from "vue";

const API_BASE = "http://127.0.0.1:8000";

const username = ref("admin");
const password = ref("admin123");
const token = ref("");
const devices = ref([]);
const error = ref("");
const loading = ref(false);

async function login() {
  error.value = "";
  loading.value = true;
  try {
    const body = new URLSearchParams();
    body.append("username", username.value);
    body.append("password", password.value);
    const response = await fetch(`${API_BASE}/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body,
    });
    if (!response.ok) {
      throw new Error("Invalid credentials");
    }
    const data = await response.json();
    token.value = data.access_token;
    await fetchDevices();
  } catch (err) {
    error.value = err.message || "Login failed";
  } finally {
    loading.value = false;
  }
}

async function fetchDevices() {
  if (!token.value) return;
  error.value = "";
  loading.value = true;
  try {
    const response = await fetch(`${API_BASE}/devices`, {
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
    if (!response.ok) {
      throw new Error("Failed to load devices");
    }
    devices.value = await response.json();
  } catch (err) {
    error.value = err.message || "Failed to fetch data";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main>
    <h1>Booksy Inventory</h1>

    <form @submit.prevent="login">
      <label>
        Username
        <input v-model="username" />
      </label>
      <label>
        Password
        <input v-model="password" type="password" />
      </label>
      <button type="submit" :disabled="loading">Login</button>
    </form>

    <p v-if="error">{{ error }}</p>

    <section v-if="token">
      <h2>Devices</h2>
      <button @click="fetchDevices" :disabled="loading">Refresh</button>
      <table border="1" cellpadding="6" cellspacing="0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Brand</th>
            <th>Purchase Date</th>
            <th>Status</th>
            <th>Notes</th>
            <th>Assigned To</th>
            <th>History</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="device in devices" :key="device.id">
            <td>{{ device.id }}</td>
            <td>{{ device.name }}</td>
            <td>{{ device.brand }}</td>
            <td>{{ device.purchase_date }}</td>
            <td>{{ device.status }}</td>
            <td>{{ device.notes }}</td>
            <td>{{ device.assigned_to }}</td>
            <td>{{ device.history }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

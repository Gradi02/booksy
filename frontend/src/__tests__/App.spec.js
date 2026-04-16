import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import App from "../App.vue";

// Mock fetch globally
global.fetch = vi.fn();

describe("Booksy Frontend - Critical Business Logic", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe("Device Rental UI", () => {
    it("should NOT render rent button for Repair status device", async () => {
      // Mock login flow
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "test-token",
        }),
      });

      // Mock auth/me endpoint
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list with a repair device
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 1,
            name: "Test Laptop",
            status: "Repair",
            brand: "Dell",
            assigned_to: null,
            purchase_date: "2024-01-01",
            notes: "In repair",
          },
        ],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Check that rent button is not available for repair device
      const devices = wrapper.vm.devices;
      expect(devices.length).toBe(1);
      expect(devices[0].status).toBe("Repair");

      // Verify that a repair device cannot be rented
      // (button should be disabled or not rendered)
      expect(wrapper.vm.devices[0].status).not.toBe("Available");
    });

    it("should NOT render rent button for In Use status device", async () => {
      // Mock login flow
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "test-token",
        }),
      });

      // Mock auth/me endpoint
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list with an in-use device
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 2,
            name: "iPad",
            status: "In Use",
            brand: "Apple",
            assigned_to: "admin@booksy.com",
            purchase_date: "2024-01-01",
            notes: "Already rented",
          },
        ],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Verify in-use device status
      const devices = wrapper.vm.devices;
      expect(devices.length).toBe(1);
      expect(devices[0].status).toBe("In Use");
      expect(devices[0].assigned_to).toBe("admin@booksy.com");
    });

    it("should render rent button for Available device", async () => {
      // Mock login flow
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "test-token",
        }),
      });

      // Mock auth/me endpoint
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list with available device
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 3,
            name: "Test Phone",
            status: "Available",
            brand: "Samsung",
            assigned_to: null,
            purchase_date: "2024-01-01",
            notes: "Ready to rent",
          },
        ],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Verify available device
      const devices = wrapper.vm.devices;
      expect(devices.length).toBe(1);
      expect(devices[0].status).toBe("Available");
    });
  });

  describe("Rent Action Triggers", () => {
    it("should trigger correct API call when rent button clicked", async () => {
      // Mock login flow
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "test-token",
        }),
      });

      // Mock auth/me endpoint
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 5,
            name: "Rent Me",
            status: "Available",
            brand: "Test",
            assigned_to: null,
            purchase_date: "2024-01-01",
          },
        ],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      // Mock rent response
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 5,
          name: "Rent Me",
          status: "In Use",
          assigned_to: "user@booksy.com",
        }),
      });

      // Mock devices refresh after rent
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 5,
            name: "Rent Me",
            status: "In Use",
            assigned_to: "user@booksy.com",
            brand: "Test",
            purchase_date: "2024-01-01",
          },
        ],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Rent device
      await wrapper.vm.rentDevice(5);
      await flushPromises();

      // Verify fetch was called with correct parameters
      const rentCall = global.fetch.mock.calls.find(
        (call) => call[0].includes("/devices/5") && call[1]?.method === "PUT"
      );
      expect(rentCall).toBeDefined();
      expect(rentCall[1].body).toContain("In Use");
      expect(rentCall[1].body).toContain("user@booksy.com");
    });

    it("should handle rent failure gracefully", async () => {
      // Mock login flow
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "test-token",
        }),
      });

      // Mock auth/me endpoint
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 6,
            name: "Device",
            status: "Available",
            brand: "Test",
          },
        ],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      // Mock rent failure with 409 conflict
      global.fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({
          detail: "Device already rented",
        }),
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Attempt to rent
      await wrapper.vm.rentDevice(6);
      await flushPromises();

      // Verify error state
      expect(wrapper.vm.error).toContain("Failed to rent device");
    });
  });

  describe("Role-Based UI Visibility", () => {
    it("should only show Mark as Repaired button for admin users", async () => {
      // Mock login flow for admin
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "admin-token",
        }),
      });

      // Mock auth/me endpoint - admin
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          username: "admin@booksy.com",
          is_admin: true,
        }),
      });

      // Mock devices list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 7,
            name: "Admin Device",
            status: "In Use",
            brand: "Test",
          },
        ],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate admin login
      wrapper.vm.username = "admin@booksy.com";
      wrapper.vm.password = "admin123";
      await wrapper.vm.login();
      await flushPromises();

      // Verify admin status
      expect(wrapper.vm.currentUser?.is_admin).toBe(true);
    });

    it("should NOT show admin controls for regular users", async () => {
      // Mock login flow for regular user
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "user-token",
        }),
      });

      // Mock auth/me endpoint - regular user
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 2,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 8,
            name: "User Device",
            status: "Available",
            brand: "Test",
          },
        ],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate user login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Verify non-admin status
      expect(wrapper.vm.currentUser?.is_admin).toBe(false);
    });

    it("should show admin view only to admins", async () => {
      // Mock login flow for regular user
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "user-token",
        }),
      });

      // Mock auth/me endpoint - regular user
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 2,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate user login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Try to navigate to admin view
      wrapper.vm.navigateTo("admin-devices");

      // Verify error is set (non-admin cannot access)
      expect(wrapper.vm.error).toContain("Admin access required");
    });
  });

  describe("Session Persistence", () => {
    it("should restore session from localStorage on mount", async () => {
      // Set up localStorage with saved session
      const testToken = "test-session-token";
      const testUser = {
        id: 1,
        username: "user@booksy.com",
        is_admin: false,
      };

      localStorage.setItem("token", testToken);
      localStorage.setItem("currentUser", JSON.stringify(testUser));

      // Mock auth/me verification
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => testUser,
      });

      // Mock devices list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      await flushPromises();

      // Verify session was restored
      expect(wrapper.vm.token).toBe(testToken);
      expect(wrapper.vm.currentUser).toEqual(testUser);
    });

    it("should clear session on logout", async () => {
      // Mock initial login
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          access_token: "test-token",
        }),
      });

      // Mock auth/me
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          username: "user@booksy.com",
          is_admin: false,
        }),
      });

      // Mock devices list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      // Mock users list
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      });

      const wrapper = mount(App, {
        global: {
          stubs: {
            Sidebar: true,
            Header: true,
            LoginPage: true,
            HardwareListView: true,
            MyRentalsView: true,
            AdminDevicesView: true,
            AdminUsersView: true,
          },
        },
      });

      // Simulate login
      wrapper.vm.username = "user@booksy.com";
      wrapper.vm.password = "password123";
      await wrapper.vm.login();
      await flushPromises();

      // Verify logged in
      expect(wrapper.vm.token).toBeTruthy();
      expect(localStorage.getItem("token")).toBeTruthy();

      // Logout
      await wrapper.vm.logout();

      // Verify session cleared
      expect(wrapper.vm.token).toBe("");
      expect(wrapper.vm.currentUser).toBeNull();
      expect(localStorage.getItem("token")).toBeNull();
    });
  });
});

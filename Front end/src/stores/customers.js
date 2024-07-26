import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useOrdersStore } from './orders'
import { updateData, urlList } from './general'
import { useAuthStore } from './auth'

export const useCustomersStore = defineStore('customers', () => {
    const inLoadingState = ref(false)
    const customersData = ref([]);
    const customersContacts = computed(() => customersData.value.flatMap(customer => customer.contactInfo));

    async function fetchCustomers() {
        inLoadingState.value = true;
        try {
            const response = await fetch(urlList.getCustomers, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                }
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const data = await response.json()
                customersData.value = data
            }
        } catch (error) {
            console.error('Error fetching customers:', error)
        }
        inLoadingState.value = false;
    }

    async function addCustomer(json) {
        const response = await fetch(urlList.addCustomer, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })
        if (!response.ok) {
            useAuthStore().logout()
        } else {
            const changes = await response.json()
            updateData(changes)
        }
    }

    async function editCustomer(json) {
        const response = await fetch(urlList.editCustomer, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })
        if (!response.ok) {
            useAuthStore().logout()
        } else {
            const changes = await response.json()
            updateData(changes)
        }
    }

    async function delCustomer(id) {
        const response = await fetch(urlList.delCustomer + id, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
            }
        });
        if (!response.ok) {
            useAuthStore().logout()
        } else {
            fetchCustomers();
            useOrdersStore().fetchOrders();
        }
    }

    return { customersData, customersContacts, fetchCustomers, addCustomer, editCustomer, delCustomer }
})

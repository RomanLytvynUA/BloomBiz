import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { urlList } from '../config'
import { useOrdersStore } from './orders'

export const useCustomersStore = defineStore('customers', () => {
    const inLoadingState = ref(false)
    const customersData = ref({});
    const customersContacts = computed(() => customersData.value.flatMap(customer => customer.contactInfo));

    async function fetchCustomers() {
        inLoadingState.value = true;
        try {
            const response = await fetch(urlList.getCustomers)
            const data = await response.json()
            customersData.value = data
        } catch (error) {
            console.error('Error fetching customers:', error)
        }
        inLoadingState.value = false;
    }

    async function addCustomer(json) {
        const response = await fetch(urlList.addCustomer, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        fetchCustomers();
    }

    async function editCustomer(json) {
        const response = await fetch(urlList.editCustomer, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        fetchCustomers();
        useOrdersStore().fetchOrders()
    }

    async function delCustomer(id) {
        const response = await fetch(urlList.delCustomer + id, {
            method: 'DELETE',
        });

        fetchCustomers();
        useOrdersStore().fetchOrders();
    }

    return { customersData, customersContacts, fetchCustomers, addCustomer, editCustomer, delCustomer }
})

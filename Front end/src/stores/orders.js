import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useGoodsStore } from './goods'
import { useAuthStore } from './auth'
import { urlList } from '../config'
import { updateData } from './general'

export const useOrdersStore = defineStore('orders', () => {
    const inLoadingState = ref(false)
    const ordersData = ref([])

    async function fetchOrders() {
        inLoadingState.value = true;
        try {
            const response = await fetch(urlList.getOrders, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                },
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const data = await response.json()
                ordersData.value = data
            }
        } catch (error) {
            console.error('Error fetching orders:', error)
        }
        inLoadingState.value = false;
    }

    async function delOrder(id) {
        try {
            const response = await fetch(urlList.delOrder + id, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                },
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                fetchOrders()
                useGoodsStore().fetchGoods()
            }
        } catch (error) {
            console.log('Error deleting order:', error)
        }
    }

    async function addOrder(data) {
        try {
            const response = await fetch(urlList.addOrder, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.log('Error while adding a new order:', error)
        }
    }

    async function editOrder(data) {
        try {
            const response = await fetch(urlList.editOrder, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.log('Error while editing a new order:', error)
        }
    }

    return { ordersData, inLoadingState, fetchOrders, delOrder, addOrder, editOrder }
})

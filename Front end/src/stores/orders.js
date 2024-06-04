import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useGoodsStore } from './goods'
import { useCustomersStore } from './customers'
import { urlList } from '../config'

export const useOrdersStore = defineStore('orders', () => {
    const ordersData = ref([])

    async function fetchOrders() {
        try {
            const response = await fetch(urlList.getOrders)
            const data = await response.json()
            ordersData.value = data
        } catch (error) {
            console.error('Error fetching orders:', error)
        }
    }

    async function delOrder(id) {
        try {
            const response = await fetch(urlList.delOrder + id, {
                method: 'DELETE'
            })

            fetchOrders()
            useGoodsStore().fetchInStockGoods()
        } catch (error) {
            console.log('Error deleting order:', error)
        }
    }

    async function addOrder(data) {
        try {
            const response = await fetch(urlList.addOrder, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })

            fetchOrders()
            useGoodsStore().fetchInStockGoods()
            useCustomersStore().fetchCustomers()
        } catch (error) {
            console.log('Error while adding a new order:', error)
        }
    }

    async function editOrder(data) {
        try {
            const response = await fetch(urlList.editOrder, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })

            fetchOrders()
            useGoodsStore().fetchInStockGoods()
        } catch (error) {
            console.log('Error while editing a new order:', error)
        }
    }

    return { ordersData, fetchOrders, delOrder, addOrder, editOrder }
})

import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useSuppliersStore } from '@/stores/suppliers'
import { useGoodsStore } from '@/stores/goods'
import { urlList } from '../config'

export const useExpensesStore = defineStore('expenses', () => {
    const expensesData = ref([])

    async function fetchExpenses() {
        try {
            const response = await fetch(urlList.getExpenses)
            const data = await response.json()
            expensesData.value = data
        } catch (error) {
            console.error('Error fetching expenses:', error)
        }
    }
    
    async function addExpense(expenseData) {
        const response = await fetch(urlList.addExpense, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(expenseData),
        })

        useSuppliersStore().fetchSuppliers();
        useGoodsStore().fetchGoods();
        fetchExpenses();
    }

    async function editExpense(expenseData) {
        const response = await fetch(urlList.editExpense, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(expenseData),
        })

        useSuppliersStore().fetchSuppliers();
        useGoodsStore().fetchGoods();
        fetchExpenses();
    }

    async function delExpense(expenseId) {
        const response = await fetch(urlList.delExpense+expenseId, {method: 'DELETE'})

        fetchExpenses()
        useGoodsStore().fetchInStockGoods()
    }

    return { expensesData, fetchExpenses, delExpense, addExpense, editExpense }
})

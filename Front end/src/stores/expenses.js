import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useGoodsStore } from '@/stores/goods'
import { updateData, urlList } from './general'
import { useAuthStore } from './auth'

export const useExpensesStore = defineStore('expenses', () => {
    const inLoadingState = ref(false);
    const expensesData = ref([])

    async function fetchExpenses() {
        inLoadingState.value = true;
        try {
            const response = await fetch(urlList.getExpenses, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                }
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const data = await response.json()
                expensesData.value = data
            }
        } catch (error) {
            console.error('Error fetching expenses:', error)
        }
        inLoadingState.value = false;
    }

    async function addExpense(expenseData) {
        const response = await fetch(urlList.addExpense, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(expenseData),
        })
        if (!response.ok) {
            useAuthStore().logout()
        } else {
            const changes = await response.json()
            updateData(changes)
        }
    }

    async function editExpense(expenseData) {
        const response = await fetch(urlList.editExpense, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(expenseData),
        })
        if (!response.ok) {
            useAuthStore().logout()
        } else {
            const changes = await response.json()
            updateData(changes)
        }
    }

    async function delExpense(expenseId) {
        const response = await fetch(urlList.delExpense + expenseId, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
            }
        })
        if (!response.ok) {
            useAuthStore().logout()
        } else {
            fetchExpenses()
            useGoodsStore().fetchGoods()
        }
    }

    return { expensesData, inLoadingState, fetchExpenses, delExpense, addExpense, editExpense }
})

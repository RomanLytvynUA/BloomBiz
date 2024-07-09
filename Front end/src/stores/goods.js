import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { urlList } from '../config'
import { updateData } from './general'
import { useAuthStore } from './auth'
import { useExpensesStore } from '@/stores/expenses'
import { useOrdersStore } from '@/stores/orders'

export const useGoodsStore = defineStore('goods', () => {
    const inLoadingState = ref(false)
    const goodsData = ref([])
    const minGoodsData = computed(() => goodsData.value.flatMap(category => category.goods))
    const goodsNames = computed(() => minGoodsData.value.flatMap(product => product.name))
    const categoriesNames = computed(() => goodsData.value.map(category => category.name));

    async function fetchGoods() {
        inLoadingState.value = true;
        try {
            const response = await fetch(urlList.getGoods, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                },
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const data = await response.json()
                goodsData.value = data
            }
        } catch (error) {
            console.error('Error fetching goods:', error)
        }
        inLoadingState.value = false;
    }

    async function createCategory(categoryData) {
        try {
            const response = await fetch(urlList.addCategory, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(categoryData),
            })

            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.error('Error creating category:', error)
        }
    }

    async function editCategory(categoryData) {
        try {
            const response = await fetch(urlList.editCategory, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(categoryData),
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.error('Error editing category:', error)
        }
    }

    async function delCategory(categoryId) {
        try {
            const response = await fetch(`${urlList.delCategory}/${categoryId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                },
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                fetchGoods()
                useOrdersStore().fetchOrders()
                useExpensesStore().fetchExpenses()
            }
        } catch (error) {
            console.error('Error deleting category:', error)
        }
    }

    async function createProduct(productData) {
        try {
            const response = await fetch(urlList.addProduct, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })

            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.error('Error creating product:', error)
        }
    }

    async function editProduct(productData) {
        try {
            const response = await fetch(urlList.editProduct, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.error('Error editing product:', error)
        }
    }

    async function delProduct(productId) {
        try {
            const response = await fetch(`${urlList.delProduct}/${productId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                },
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                fetchGoods()
                useOrdersStore().fetchOrders()
                useExpensesStore().fetchExpenses()
            }
        } catch (error) {
            console.error('Error deleting product:', error)
        }
    }

    async function submitDecommission(productData) {
        try {
            const response = await fetch(urlList.addDecommission, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.error('Error adding a decommission:', error)
        }
    }

    async function setProductPrice(productData) {
        try {
            const response = await fetch(urlList.setProductPrice, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const changes = await response.json()
                updateData(changes)
            }
        } catch (error) {
            console.error('Error setting product price:', error)
        }
    }

    async function resetProductPrices() {
        try {
            const response = await fetch(urlList.resetProductPrices, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                    'Content-Type': 'application/json',
                },
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                fetchGoods()
            }
        } catch (error) {
            console.error('Error resetting product prices:', error)
        }
    }

    return {
        goodsData, goodsNames, inLoadingState, categoriesNames, minGoodsData, fetchGoods, submitDecommission,
        setProductPrice, createProduct, editProduct, delProduct, createCategory, editCategory, delCategory, resetProductPrices,
    }
})

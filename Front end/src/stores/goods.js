import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { urlList } from '../config'

export const useGoodsStore = defineStore('goods', () => {
    const goodsData = ref([])
    const inStockGoodsData = ref([])
    const minGoodsData = computed(() => goodsData.value.flatMap(category => category.goods))
    const categoriesNames = computed(() => goodsData.value.map(category => category.name));

    async function fetchGoods() {
        try {
            const response = await fetch(urlList.getGoods)
            const data = await response.json()
            goodsData.value = data

            fetchInStockGoods()
        } catch (error) {
            console.error('Error fetching goods:', error)
        }
    }

    async function createProduct(productData) {
        try {
            await fetch(urlList.addProduct, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })
            fetchGoods()
        } catch (error) {
            console.error('Error crearing product:', error)
        }
    }

    async function editProduct(productData) {
        try {
            await fetch(urlList.editProduct, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })
            fetchGoods()
        } catch (error) {
            console.error('Error editing product:', error)
        }
    }

    async function delProduct(productId) {
        try {
            await fetch(`${urlList.delProduct}/${productId}`, {
                method: 'DELETE',
            })
            fetchGoods()
        } catch (error) {
            console.error('Error editing product:', error)
        }
    }

    async function fetchInStockGoods() {
        try {
            const response = await fetch(urlList.getInStockGoods)
            const data = await response.json()
            inStockGoodsData.value = data
        } catch (error) {
            console.error('Error fetching in stock goods:', error)
        }
    }

    async function submitDecommission(productData) {
        try {
            const response = await fetch(urlList.addDecommission, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })

            fetchInStockGoods()
        } catch (error) {
            console.error('Error adding a decommission:', error)
        }
    }

    async function setProductPrice(productData) {
        try {
            const response = await fetch(urlList.setProductPrice, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })

            fetchInStockGoods()
        } catch (error) {
            console.error('Error editing product price:', error)
        }
    }
    return { goodsData, inStockGoodsData, categoriesNames, minGoodsData, fetchGoods, fetchInStockGoods, submitDecommission, setProductPrice, createProduct, editProduct, delProduct }
})

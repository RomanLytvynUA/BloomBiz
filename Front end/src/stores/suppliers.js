import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { urlList } from '../config'
import { updateData } from './general'
import { useExpensesStore } from './expenses'
import { useGoodsStore } from './goods'

export const useSuppliersStore = defineStore('suppliers', () => {
    const inLoadingState = ref(false)
    const suppliersData = ref([])

    const suppliersNames = computed(() => suppliersData.value.map(supplier => supplier.name))

    async function fetchSuppliers() {
        inLoadingState.value = true;
        try {
            const response = await fetch(urlList.getSuppliers)
            const data = await response.json()
            suppliersData.value = data
        } catch (error) {
            console.error('Error fetching suppliers:', error)
        }
        inLoadingState.value = false;
    }

    async function delSupplier(id) {
        const response = await fetch(urlList.delSupplier + id, {
            method: 'DELETE',
        });

        fetchSuppliers();
        useExpensesStore().fetchExpenses();
        useGoodsStore().fetchGoods();
    }

    async function addSupplier(json) {
        const response = await fetch(urlList.addSupplier, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        const changes = await response.json();
        updateData(changes);
    }

    async function editSupplier(json) {
        const response = await fetch(urlList.editSupplier, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        const changes = await response.json();
        updateData(changes);
    }


    return { inLoadingState, suppliersData, fetchSuppliers, delSupplier, addSupplier, editSupplier, suppliersNames }
})

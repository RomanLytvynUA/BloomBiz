import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { urlList } from '../config'

export const useSuppliersStore = defineStore('suppliers', () => {
    const suppliersData = ref([])

    const suppliersNames = computed(() => suppliersData.value.map(supplier => supplier.name))

    async function fetchSuppliers() {
        try {
            const response = await fetch(urlList.getSuppliers)
            const data = await response.json()
            suppliersData.value = data
        } catch (error) {
            console.error('Error fetching suppliers:', error)
        }
    }

    async function delSupplier(id) {
        const response = await fetch(urlList.delSupplier+id, {
          method: 'DELETE',
        });
      
        fetchSuppliers();
    }

    async function addSupplier(json) {
        const response = await fetch(urlList.addSupplier, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        fetchSuppliers();
    }

    async function editSupplier(json) {
        const response = await fetch(urlList.editSupplier, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        fetchSuppliers();
    }
      

    return { suppliersData, fetchSuppliers, delSupplier, addSupplier, editSupplier, suppliersNames }
})

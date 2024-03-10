<template>
    <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center list-group-item-secondary">
            <p class="my-auto">Елементи замовлення</p>
            <div class="dropdown">
                <button class="btn btn-sm btn-success" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    +
                </button>
                <ul class="dropdown-menu">
                    <li v-for="newCategory in existingCategories" :key="newCategory">
                        <button 
                            class="dropdown-item" 
                            @click.prevent="categories.push(newCategory)"
                            :disabled="categories.find((category) => category === newCategory)"
                        >
                            {{ newCategory }}
                        </button>
                    </li>
                </ul>
                </div>
        </li>
        <li v-for="category in categories" :data-id="category" class="list-group-item text-center align-middle" :key="'category'+category">
            <h6
            style="display: inline-block; cursor: pointer;" 
            onmouseover="this.style.textDecoration='line-through'; this.style.color='red'" 
            onmouseout="this.style.textDecoration='none'; this.style.color='black'"
            @click.prevent="categories.splice(categories.findIndex((addedCategory) => addedCategory === category), 1); calculateTotalPrice(category, 0);
             recordElements(category, []); prefilledElementsData = {}"
            >
                {{ category }}
            </h6>
            <ElementsTable @rows-changed="(category, data) => {recordElements(category, data)}"
                :ref="'elementsTable'+category" 
                @total-price-changed="(category, price, emitChanges) => calculateTotalPrice(category, price, emitChanges)" 
                :category="category" :prefilledElements="prefilledElementsData[category] ? prefilledElementsData[category] : []"
            />
        </li>
    </ul>
</template>

<script setup>
import { computed, ref, onMounted, watch, watchEffect } from 'vue';

import ElementsTable from './ElementsTable.vue';

import { useGoodsStore } from '@/stores/goods';

const existingCategories = computed(() => useGoodsStore().categoriesNames)

const emit = defineEmits(['totalPriceChanged', 'elementsChanged'])
const categories = ref([])
const prefilledElementsData = ref({})

const totalPrice = ref(0)
const totalPrices = ref({})
const elementsList = ref({})

function calculateTotalPrice(category=null, price=null, emitChanges=true) {
    if(category !== null && price !== null){
        totalPrices.value[category] = price 
    }
    totalPrice.value = Object.values(totalPrices.value).reduce((a, b) => a + b, 0)
    if (emitChanges) {
        emit('totalPriceChanged', totalPrice.value)
    }
}

function recordElements(category=null, data=null) {
    if(category !== null && data !== null){
        elementsList.value[category] = data
        emit('elementsChanged', elementsList.value)
    }
}

function reset() {
    categories.value = []
    totalPrice.value = 0
    totalPrices.value = {}
    elementsList.value = {}
    prefilledElementsData.value = {}
    emit('elementsChanged', elementsList.value)
}

async function setNewData(categoriesList, elementsObject) {
    // MUST wait till new prefilledElementsData is loaded before categories
    // so all ElementsTables are recreated with new prefilledElementsData
    prefilledElementsData.value = await elementsObject
    categories.value = categoriesList

    emit('elementsChanged', elementsList.value)
}

defineExpose({totalPrice, reset, setNewData})
</script>

<style scoped>
.list-group-item-secondary {
    background-color: #f8f9fa;
    color: #212529;
}
.dropdown-item:focus {
    background-color: #fff;
    color: #fff; 
}
</style>
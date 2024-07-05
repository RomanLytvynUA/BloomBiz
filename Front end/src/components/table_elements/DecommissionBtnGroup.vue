<template>
    <div class="input-group input-group-sm flex-nowrap">
        <input v-model="quantityInput" type="number" class="form-control" placeholder="Кількість"
            style="min-width: 90px;">
        <button class="btn btn-sm btn-outline-danger opacity-75" type="button"
            @click="submitDecommission">Списати</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useGoodsStore } from '@/stores/goods';

const todaysDate = new Date().toISOString().split('T')[0];
const props = defineProps(['productId']);
const quantityInput = ref('')

function submitDecommission() {
    if (quantityInput.value) {
        const productData = { 'date': todaysDate, 'productId': props.productId, 'quantity': quantityInput.value }
        useGoodsStore().submitDecommission(productData)
        quantityInput.value = ''
    }
}

</script>
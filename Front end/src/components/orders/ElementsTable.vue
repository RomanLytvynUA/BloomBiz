<template>
    <table class="table table-bordered text-center table-sm align-middle">
        <thead>
            <tr>
                <th scope="col" width="10%"></th>
                <th scope="col" width="35%" class="small">Товар</th>
                <th scope="col" width="15%" class="small">Кількість</th>
                <th scope="col" width="15%" class="small">Ціна</th>
                <th scope="col" width="25%" class="small">Всього</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(row, index) in rows" :key="row">
                <td>
                    <button type="button" class="btn btn-outline-danger btn-sm"
                        @click="rows.splice(index, 1); calculateTotalPrice()">X</button>
                </td>
                <td>
                    <Autocomplete :small="false" :name="'orderElement' + index"
                        @valueSelected="(newValue) => handleProductSelect(index, newValue)"
                        :preselectedValue="rows[index].product" :options="row.options" customOptionLabel=""
                        divClasses="" />
                </td>
                <td>
                    <input v-model="rows[index].quantity" @input="calculateTotalPrice()" type="number"
                        class="form-control" :name="'productQuantity' + index" placeholder="0">
                </td>
                <td>
                    <input v-model="rows[index].price" @input="calculateTotalPrice()" type="number" class="form-control"
                        :name="'productPrice' + index" placeholder="0">
                </td>
                <td>
                    <input type="text" class="form-control" :name="'productTotal' + index"
                        :value="rows[index].quantity * rows[index].price" disabled>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <button type="button" class="btn btn-outline-success" @click="addRow()"
                        :disabled="category === null">+</button>
                </td>
                <td colspan="1">
                    <input v-model="totalPrice" type="number" class="form-control" name="total">
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup>
import { ref, computed, watch, watchEffect } from 'vue';
import { useGoodsStore } from '@/stores/goods';
import { useSettingsStore } from '@/stores/settings';

import Autocomplete from '../form_elements/Autocomplete.vue'

const emit = defineEmits(['totalPriceChanged', 'rowsChanged']);
const props = defineProps({
    category: String,
    prefilledElements: {
        type: Array,
        default: [],
    },
});
const hideOutOfStock = computed(() => useSettingsStore().settingsData.ordersHideOutOfStock === "true" ? true : false);
const goodsToIgnore = computed(() => useSettingsStore().settingsData.ordersGoodsToIgnore);

const goodsData = computed(() => useGoodsStore().inStockGoodsData.filter((product) => product.category === props.category));
const totalPrice = ref(0);
const rows = ref(props.prefilledElements.map(element => ({
    options: goodsData.value.filter((product) => (product.quantity >= 1 || !hideOutOfStock.value) && (!goodsToIgnore.value.includes(product.product))).map(product => product.product),
    product: computed(() => {
        const product = useGoodsStore().minGoodsData.find(prod => prod.id === element.product);
        return product ? product.name : "-";
    }),
    quantity: element.quantity,
    price: element.price,
})));

function calculateTotalPrice(emitChanges = true) {
    totalPrice.value = rows.value.reduce((total, row) => total + row.quantity * row.price, 0);
    emit('totalPriceChanged', props.category, totalPrice.value, emitChanges);
}
calculateTotalPrice(false);

function addRow(value = '', quantity = '', price = '') {
    rows.value.push({
        options: goodsData.value.filter((product) => (product.quantity >= 1 || !hideOutOfStock.value) && (!goodsToIgnore.value.includes(product.product))).map(product => product.product),
        product: value,
        quantity: quantity,
        price: price,
    });
}

function handleProductSelect(index, newValue) {
    // MUST use a copy of a row to avoid ""'set' on proxy" error
    const updatedRow = { ...rows.value[index] };

    updatedRow.product = newValue;
    updatedRow.price = goodsData.value.find((product) => product.product === newValue).price;

    // Update the row in the array
    rows.value[index] = updatedRow;

    calculateTotalPrice();
}

function reset() {
    rows.value = [];
}

watch(rows.value, () => {
    emit('rowsChanged', props.category, rows.value.map((row) => ({ 'product': row.product, 'price': row.price, 'quantity': row.quantity })));
}, { deep: true });
emit('rowsChanged', props.category, rows.value.map((row) => ({ 'product': row.product, 'price': row.price, 'quantity': row.quantity })));

defineExpose({ rows, totalPrice, addRow, reset });
</script>

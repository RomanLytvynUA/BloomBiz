<template>
    <table class="table table-bordered text-center table-sm align-middle">
        <thead>
            <tr>
                <th scope="col" width="70px"></th>
                <th scope="col" width="30%" class="small">Товар</th>
                <th scope="col" width="15%" class="small">Кількість</th>
                <th scope="col" width="20%" class="small">Ціна</th>
                <th scope="col" width="20%" class="small">Всього</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(row, index) in rows" :key="row">
                <td>
                    <button type="button" class="btn btn-outline-danger btn-sm" @click="rows.splice(index, 1); calculateTotalPrice()">X</button>
                </td>
                <td>
                    <SelectField @valueSelected="(newValue) => rows[index].product = newValue" :name="'expenseElement'+index" :preselectedValue="rows[index].product" :options="row.options" customOptionValue="+ Додати новий" divClasses="" />
                </td>
                <td>
                    <input v-model="rows[index].quantity" @input="calculateTotalPrice()" type="number" class="form-control" :name="'productQuantity'+index" placeholder="0">
                </td>
                <td>
                    <input v-model="rows[index].price" @input="calculateTotalPrice()" type="number" class="form-control" :name="'productPrice'+index" placeholder="0">
                </td>
                <td>
                    <input type="number" class="form-control" :name="'productTotal'+index" :value="rows[index].quantity * rows[index].price" disabled>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <button type="button" class="btn btn-outline-success" @click="addRow(category)" :disabled="category === null">+</button>
                </td>
                <td colspan="1">
                    <input v-model="totalPrice" type="number" class="form-control" name="total">
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

import { useGoodsStore } from '@/stores/goods'

import SelectField from '../form_elements/SelectField.vue'

const props = defineProps(['category', 'rows']);
const goodsData = computed(() => useGoodsStore().goodsData)
const totalPrice = ref(0)

const rows = ref(props.rows)

function calculateTotalPrice() {
    totalPrice.value = rows.value.reduce((total, row) => {
    return total + row.quantity * row.price;
  }, 0);
}

function addRow(category, value='', quantity='', price='') {

    rows.value.push(
        {
            options: category !== 'custom' ? goodsData.value.find(rawCategory => rawCategory.name === category).goods.map(product => product.name) : [],
            product: value,
            quantity: quantity,
            price: price,
        }
    )
}

function reset() {
    rows.value = []
}

defineExpose({ rows, totalPrice, addRow, reset })
</script>

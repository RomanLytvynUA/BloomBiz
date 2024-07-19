<template>
    <table class="table table-bordered text-center table-sm align-middle">
        <thead>
            <tr>
                <th scope="col" width="10%"></th>
                <th scope="col" width="35%" class="small">{{ t('general.elementsTableHeaders.product') }}</th>
                <th scope="col" width="15%" class="small">{{ t('general.elementsTableHeaders.quantity') }}</th>
                <th scope="col" width="15%" class="small">{{ t('general.elementsTableHeaders.price') }}</th>
                <th scope="col" width="25%" class="small">{{ t('general.elementsTableHeaders.total') }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(row, index) in rows" :key="row">
                <td>
                    <button type="button" class="btn btn-outline-danger btn-sm"
                        @click="rows.splice(index, 1); calculateTotalPrice()">X</button>
                </td>
                <td>
                    <Autocomplete :small="false" :name="'expenseElement' + index"
                        @valueSelected="(newValue) => rows[index].product = newValue"
                        :preselectedValue="rows[index].product" :options="row.options"
                        :customOptionLabel="t('general.customOptions.customProductText')" divClasses="" />
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
                    <input type="number" class="form-control" :name="'productTotal' + index"
                        :value="rows[index].quantity * rows[index].price" disabled>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <button type="button" class="btn btn-outline-success" @click="addRow(category)"
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
import { ref, computed, watch } from 'vue';

import { useGoodsStore } from '@/stores/goods'
import { useSettingsStore } from '@/stores/settings';

import Autocomplete from '../form_elements/Autocomplete.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps(['category', 'rows']);
const goodsData = computed(() => useGoodsStore().goodsData)
const goodsToIgnore = computed(() => useSettingsStore().settingsData.expensesGoodsToIgnore);
const suppliersToIgnore = computed(() => useSettingsStore().settingsData.expensesSuppliersToIgnore);
const totalPrice = ref(0)


const rows = ref(props.rows)

function calculateTotalPrice() {
    totalPrice.value = rows.value.reduce((total, row) => {
        return total + row.quantity * row.price;
    }, 0);
}

function addRow(category, value = '', quantity = '', price = '') {
    rows.value.push(
        {
            options: category !== 'custom' ? goodsData.value.find(rawCategory => rawCategory.name === category).goods
                .filter((product) => !goodsToIgnore.value.includes(product.name)).map(product => product.name) : [],
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

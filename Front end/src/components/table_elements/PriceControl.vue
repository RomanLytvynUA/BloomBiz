<template>
    <div :style="{ display: mode === 'view' ? '' : 'none' }"
        class="input-group input-group-sm flex-nowrap justify-content-center">
        <span class="input-group-text" style="width: 40px;">{{ prefilledValue }}</span>
        <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" style="max-width: 26px;"
            data-bs-toggle="dropdown" aria-expanded="false"></button>
        <ul class="dropdown-menu">
            <li><button class="dropdown-item" type="button" @click.prevent="mode = 'edit'">Змінити</button></li>
            <li><button class="dropdown-item" type="button"
                    @click.prevent="handlePriceChange(price = 'RESET')">Скинути</button></li>
        </ul>
    </div>
    <div :style="{ display: mode === 'edit' ? '' : 'none' }" class="input-group input-group-sm justify-content-center">
        <input v-model="customPrice" type="text" class="form-control" style="max-width: 40px;">
        <button type="button" class="btn btn-secondary btn-save" style="max-width: 26px;"
            @click.prevent="handlePriceChange()">✓</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useGoodsStore } from '../../stores/goods';

const props = defineProps({
    prefilledValue: String,
    productId: String,
});

const mode = ref('view')
const customPrice = ref(props.prefilledValue)

function handlePriceChange(price = customPrice.value) {
    const data = { "product_id": props.productId, "price": price }
    useGoodsStore().setProductPrice(data)
}

</script>

<style scoped>
.input-group-text {
    background-color: white;
}

.btn.dropdown-toggle {
    background-color: #f8f9fa;
    border-color: #c6c7c8;
}

.dropdown-item:focus {
    background-color: #fff;
    color: #fff;
}

.btn.dropdown-toggle::after {
    border-top-color: #c6c7c8;
    /* Custom arrow color */
}

.dropdown-menu {
    min-width: 100px;
}

.btn-save {
    background-color: #f8f9fa;
    color: #c6c7c8;
    border-color: #c6c7c8;
}

.btn-save:active {
    background-color: #c6c7c8;
    color: #f8f9fa;
    border-color: #c6c7c8;
}
</style>

<template>
    <label class="form-label">{{ label }}</label>
    <div v-if="!constant" class="input-group mb-3">
        <select v-if="!customCategory" v-model="categorySelect" class="form-select" name="category" style="width: 85%">
            <option v-if="customOption" style="background-color: green;">+ Додати нову</option>
            <option v-else hidden></option>
            <option v-for="category in categories" :key="category.id" :value="category.name">{{ category.name }}
            </option>
        </select>
        <input v-if="customCategory" v-model="customCategoryInput" type="text" name="category" class="form-control"
            style="width: 85%;">

        <input class="form-control" v-model="categoryUnits" name="categoryUnits" style="width: 15%"
            :disabled="!customCategory">
    </div>
    <div v-else class="input-group mb-3">
        <input :value="constant.category" class="form-select" style="width: 85%" disabled>
        <input :value="constant.units" class="form-control" style="width: 15%" disabled>
    </div>
</template>

<script setup>
import { computed, watch, ref, defineExpose } from 'vue';
import { useGoodsStore } from '@/stores/goods';

const emit = defineEmits(['categoryChanged', 'unitsChanged'])
const props = defineProps({
    constant: Object,
    label: { type: String, default: 'Категорія: ' },
    customOption: { type: Boolean, default: true },
    custom: { type: Boolean, default: false },
    prefilledName: { type: String, default: '' },
    prefilledUnits: { type: String, default: '' }
})

const categories = computed(() => useGoodsStore().goodsData)
const categorySelect = ref('')
const categoryUnits = ref(props.prefilledUnits)
const customCategory = ref(props.custom)
const customCategoryInput = ref(props.prefilledName)

const reset = () => {
    customCategory.value = false
    categorySelect.value = null
    categoryUnits.value = ''
}


watch(categorySelect, () => {
    if (categorySelect.value === '+ Додати нову') {
        customCategory.value = true
        categoryUnits.value = '';

        emit('categoryChanged', 'custom')
    } else {
        const selectedCategoryUnits = categories.value.find((category) => category.name === categorySelect.value)
        selectedCategoryUnits ? categoryUnits.value = selectedCategoryUnits.units : '';

        emit('categoryChanged', categorySelect.value)
        emit('unitsChanged', selectedCategoryUnits.units)
    }
})

defineExpose({
    reset,
    customCategoryInput,
    categoryUnits,
    categorySelect,
})
</script>

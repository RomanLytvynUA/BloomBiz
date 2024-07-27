<template>
    <label class="form-label">{{ label }}</label>
    <!-- Usable input -->
    <div v-if="!constant" class="input-group mb-3">
        <!-- Select -->
        <select v-if="!customCategory" v-model="selectedCategory" class="form-select" name="category"
            style="width: 75%">
            <option v-if="customOption" style="background-color: green;">{{
        t('general.customOptions.customCategoryText') }}
            </option>
            <option v-else hidden></option>
            <option v-for="category in categories" :key="category.id" :value="category.name">{{ category.name }}
            </option>
        </select>

        <!-- Custom option -->
        <input v-if="customCategory" v-model="customCategoryInput" type="text" name="category" class="form-control"
            style="width: 75%;">

        <!-- Units input -->
        <input class="form-control" v-model="categoryUnits" name="categoryUnits" style="width: 25%"
            :disabled="!customCategory">
    </div>
    <!-- Disabled input -->
    <div v-else class="input-group mb-3">
        <input :value="constant.category" class="form-select" style="width: 75%" disabled>
        <input :value="constant.units" class="form-control" style="width: 25%" disabled>
    </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue';
import { useGoodsStore } from '@/stores/goods';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const emit = defineEmits(['categoryChanged', 'unitsChanged'])
const props = defineProps({
    constant: Object,
    label: { type: String, default: '' },
    customOption: { type: Boolean, default: true },
    custom: { type: Boolean, default: false },
    prefilledName: { type: String, default: '' },
    prefilledUnits: { type: String, default: '' }
})

const categories = computed(() => useGoodsStore().goodsData)
const selectedCategory = ref('')
const categoryUnits = ref(props.prefilledUnits)
const customCategory = ref(props.custom)
const customCategoryInput = ref(props.prefilledName)

const reset = () => {
    customCategory.value = false
    selectedCategory.value = null
    categoryUnits.value = ''
}


watch(selectedCategory, () => {
    if (selectedCategory.value === t('general.customOptions.customCategoryText')) {
        // change input to custom
        customCategory.value = true
        categoryUnits.value = '';
        emit('categoryChanged', 'custom')
    } else {
        const selectedCategoryUnits = categories.value.find((category) => category.name === selectedCategory.value)
        selectedCategoryUnits ? categoryUnits.value = selectedCategoryUnits.units : '';

        emit('categoryChanged', selectedCategory.value)
        emit('unitsChanged', selectedCategoryUnits ? selectedCategoryUnits.units : '')
    }
})

defineExpose({
    reset,
    customCategoryInput,
    categoryUnits,
    selectedCategory,
})
</script>

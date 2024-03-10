<template>
    <label class="form-label">Категорія: </label>
    <div v-if="!constant" class="input-group mb-3">
        <select v-if="!customCategory" v-model="categorySelect" class="form-select" name="category" style="width: 85%">
            <option style="background-color: green;">+ Додати нову</option>
            <option v-for="category in categories" :key="category.id" :value="category.name">{{ category.name }}</option>
        </select>
        <input v-if="customCategory" type="text" name="category" class="form-control" style="width: 85%;">

        <input class="form-control" v-model="categoryUnits" name="categoryUnits" style="width: 15%" :disabled="!customCategory">
    </div>
    <div v-else class="input-group mb-3">
        <input :value="constant.category" class="form-select" style="width: 85%" disabled>
        <input :value="constant.units" class="form-control" style="width: 15%" disabled>
    </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue';
import { useGoodsStore } from '@/stores/goods';

const emit = defineEmits(['categoryChanged'])
const props = defineProps({
  constant: Object,
})

const categories = computed(() => useGoodsStore().goodsData)
const categorySelect = ref('')
const categoryUnits = ref('')
const customCategory = ref(false)

const reset = () => {
    customCategory.value = false
    categorySelect.value = null
    categoryUnits.value = ''
}

watch(categorySelect, () => {
    if(categorySelect.value === '+ Додати нову') {
        customCategory.value = true
        categoryUnits.value = '';

        emit('categoryChanged', 'custom')
    } else {
        const selectedCategoryUnits = categories.value.find((category) => category.name === categorySelect.value)

        
        selectedCategoryUnits ? categoryUnits.value = selectedCategoryUnits.units : '';
        emit('categoryChanged', categorySelect.value)
    }
})

defineExpose({
    reset
})
</script>

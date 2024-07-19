<template>
    <div class="list-group mb-2">
        <div class="list-group-item">
            <div class="row align-items-center">
                <div class="col">
                    <p class="mb-0">{{ title }}</p>
                    <p class="text-muted mb-0">{{ info }}</p>
                </div>
                <div class="col-auto" style="padding: 5px;">
                    <div v-if="type === 'switch'" class="form-check form-switch d-flex justify-content-center">
                        <input class="form-check-input" type="checkbox" role="switch" v-model="switchInput">
                    </div>
                    <div v-if="type === 'input'">
                        <input type="number" class="form-control" style="width: 70px;" v-model="intInput" />
                    </div>
                    <div v-if="type === 'resetBtn'">
                        <button class="btn btn-outline-danger btn-sm" data-bs-toggle="modal" :data-bs-target="modal">{{
                        t('general.resetBtnText') }}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps({
    title: String,
    info: String,
    type: String,
    value: String,
    modal: String,
})
const emit = defineEmits(['optionChanged'])

const switchInput = ref(props.value);
const intInput = ref(props.value);

watch(() => props.value, intInput.value = props.value)
watch(switchInput, (newVal) => {
    emit('optionChanged', newVal);
})

watch(intInput, (newVal) => {
    emit('optionChanged', newVal);
})
defineExpose({ switchInput, intInput })
</script>
<style scoped>
.form-check-input {
    cursor: pointer;
}
</style>
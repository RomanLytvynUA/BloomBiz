<template>
    <div class="list-group mb-2">
        <div class="list-group-item">
            <div class="row align-items-center">
                <div class="col">
                    <p class="mb-0">{{ title }}</p>
                    <p class="text-muted mb-0">{{ info }}</p>
                </div>
                <div class="col-auto">
                    <div class="input-group">
                        <div v-if="type === 'switch'" class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" role="switch" v-model="switchInput">
                        </div>
                        <div v-if="type === 'input'" class="input-group">
                            <input type="number" class="form-control" style="width: 70px;" v-model="intInput" />
                        </div>
                        <div v-if="type === 'btn'" class="input-group">
                            <button class="btn btn-outline-danger btn-sm" data-bs-toggle="modal"
                                :data-bs-target="modal">{{ value }}</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue';

const props = defineProps({
    title: String,
    info: String,
    type: String,
    value: String,
    modal: String,
})
const emit = defineEmits(['optionChanged'])

const switchInput = ref(false);
const intInput = ref(false);

watch(() => props.value, intInput.value = props.value)
watch(switchInput, (newVal) => {
    emit('optionChanged', newVal);
})

watch(intInput, (newVal) => {
    emit('optionChanged', newVal);
})
</script>
<style scoped>
.form-check-input {
    cursor: pointer;
}
</style>
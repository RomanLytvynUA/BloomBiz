<template>
    <div class="modal fade" :id="idPrefix + 'IgnoreModal'" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <Autocomplete ref="select" :label="labelName" customOptionLabel="" :options="options" />
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                    <button type="submit" class="btn btn-primary" @click.prevent="validateStatus()">Зберегти</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Autocomplete from '../../form_elements/Autocomplete.vue'

const select = ref(null)
const emit = defineEmits(['statusAdded'])
const props = defineProps({
    idPrefix: String,
    title: String,
    labelName: String,
    options: Array,
})

function validateStatus() {
    if (select.value.input !== "") {
        select.value.inputElement.classList.remove('is-invalid');
        emit('dataSelected', select.value.input)
        select.value.reset()
        $(`#${props.idPrefix}IgnoreModal`).modal('hide');
    } else {
        select.value.inputElement.classList.add('is-invalid');
    }
}
</script>
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
                    <button type="submit" class="btn btn-success" @click.prevent="validateStatus()">{{
        t("general.addBtnText") }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Autocomplete from '../../form_elements/Autocomplete.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

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

<style scoped>
.modal-body :last-child {
    margin-bottom: 0 !important;
}

.modal-footer {
    padding: 0;
}

.modal-footer>button {
    width: 100%;
    height: 100%;
    margin: 0;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
</style>
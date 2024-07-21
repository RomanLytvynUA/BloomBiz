<template>
    <div class="modal fade" id="addStatusModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t("dashboard.settings.orders.statusModalTitle") }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="statusInput" class="form-label">{{
                        t("dashboard.settings.orders.statusModalInputLabel") }}</label>
                        <input ref="statusInput" type="text" class="form-control" id="statusInput">
                    </div>
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
import { computed, ref, onMounted, watch } from 'vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const statusInput = ref(null)
const emit = defineEmits(['statusAdded'])

function validateStatus() {
    if (statusInput.value.value !== "") {
        statusInput.value.classList.remove('is-invalid');
        emit('statusAdded', statusInput.value.value)
        statusInput.value.value = "";
        $("#addStatusModal").modal('hide');
    } else {
        statusInput.value.classList.add('is-invalid');
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
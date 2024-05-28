<template>
    <div class="modal fade" id="addStatusModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Додати новий статус замовлення</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="statusInput" class="form-label">Назва статусу</label>
                        <input ref="statusInput" type="text" class="form-control" id="statusInput">
                    </div>
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
import { computed, ref, onMounted, watch } from 'vue';

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
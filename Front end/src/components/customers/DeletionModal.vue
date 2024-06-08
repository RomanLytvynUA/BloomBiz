<template>
    <div class="modal fade" id="delCustomerModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Ви впевненні?</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Всі данні пов'язані з цим клієнтом будуть видалені, цю дію не можна відмінити.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
                        @click="deleteCustomer()">Видалити</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCustomersStore } from '@/stores/customers';

const selectedCustomerId = ref(null);

onMounted(() => {
    const modalElement = document.getElementById('delCustomerModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        selectedCustomerId.value = btn.parentElement.getAttribute('data-customer-id');
    });
});

function deleteCustomer() {
    useCustomersStore().delCustomer(selectedCustomerId.value);
}
</script>
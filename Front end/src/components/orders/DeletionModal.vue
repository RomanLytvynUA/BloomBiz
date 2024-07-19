<template>
    <div class="modal fade" id="delOrderModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('orders.deletionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>{{ t('orders.deletionModalConfirmationMessage') }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{
                        t('general.cancelBtnText') }}</button>
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteOrder()">{{
                        t('orders.delBtnText') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useOrdersStore } from '@/stores/orders';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const ordersStore = useOrdersStore();
const selectedOrderId = ref(null);

onMounted(() => {
    const modalElement = document.getElementById('delOrderModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        selectedOrderId.value = btn.parentElement.getAttribute('data-order-id');
    });
});

function deleteOrder() {
    ordersStore.delOrder(selectedOrderId.value);
}
</script>
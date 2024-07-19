<template>
    <div class="modal fade" id="delSupplierModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('suppliers.deletionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>{{ t('suppliers.deletionModalConfirmationMessage') }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{
                        t('general.cancelBtnText') }}</button>
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteSupplier">{{
                        t('general.delBtnText') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useSuppliersStore } from '@/stores/suppliers';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const suppliersStore = useSuppliersStore();
const selectedSupplierId = ref(null);

onMounted(() => {
    const modalElement = document.getElementById('delSupplierModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        selectedSupplierId.value = btn.parentElement.getAttribute('data-supplier-id');
    });
});

function deleteSupplier() {
    suppliersStore.delSupplier(selectedSupplierId.value);
}
</script>
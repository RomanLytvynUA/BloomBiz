<template>
    <div class="modal fade" id="delProductModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Ви впевненні?</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Цю дію не можна відмінити.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
                        @click="deleteProduct()">Видалити</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// import { useSuppliersStore } from '@/stores/suppliers';

const selectedProductId = ref(null);

onMounted(() => {
    const modalElement = document.getElementById('delProductModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        selectedProductId.value = btn.parentElement.getAttribute('data-product-id');
    });
});

function deleteProduct() {
    // suppliersStore.delSupplier(selectedSupplierId.value);
    console.log(selectedProductId.value)
}
</script>
<template>
    <div class="modal fade" id="editSupplierModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('suppliers.editionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="editSupplierForm">
                    <div class="modal-body">
                        <InputField :label="t('suppliers.formFields.nameLabel')" type="text" name="name"
                            :value="oldSupplierData ? oldSupplierData.name : ''" />
                        <InputField :label="t('suppliers.formFields.contactInfoLabel')" type="text" name="contactInfo"
                            :value="oldSupplierData ? oldSupplierData.contactInfo : ''" />
                        <InputField :label="t('suppliers.formFields.additionalLabel')" type="text" name="additional"
                            :value="oldSupplierData ? oldSupplierData.additional : ''" />
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-success" @click.prevent="validateSupplier">{{
                        t('general.saveBtnText') }}</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import InputField from '../form_elements/InputField.vue';
import { useSuppliersStore } from '@/stores/suppliers';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const suppliersStore = useSuppliersStore();
const supplierId = ref(null)
const oldSupplierData = computed(() => suppliersStore.suppliersData.find(supplier => supplier.id === Number(supplierId.value)))

onMounted(() => {
    const modalElement = document.getElementById('editSupplierModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        supplierId.value = btn.parentElement.getAttribute('data-supplier-id');
    });
});

function validateSupplier() {
    let valid = true
    const form = document.getElementById('editSupplierForm')

    // add 'is-invalid' class to every element of form that has no value
    for (const element of form.elements) {
        if (element.tagName === 'INPUT' && !element.value && element.name !== 'additional') {
            element.classList.add('is-invalid');
            valid = false
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid) {
        const suppliersStore = useSuppliersStore();
        const supplierData = new FormData(form);

        let json = {}
        json['id'] = supplierId.value;
        supplierData.forEach((value, key) => {
            json[key] = value;
        });

        $(document.getElementById('editSupplierModal')).modal('hide');
        suppliersStore.editSupplier(json);
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
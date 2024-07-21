<template>
    <div class="modal fade" id="addSupplierModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('suppliers.additionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="newSupplierForm">
                    <div class="modal-body">
                        <InputField :label="t('suppliers.formFields.nameLabel')" type="text" name="name" />
                        <InputField :label="t('suppliers.formFields.contactInfoLabel')" type="text"
                            name="contactInfo" />
                        <InputField :label="t('suppliers.formFields.additionalLabel')" type="text" name="additional" />
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-success" @click.prevent="validateSupplier">{{
                        t('general.addBtnText') }}</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import InputField from '../form_elements/InputField.vue'
import { useSuppliersStore } from '@/stores/suppliers';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

function validateSupplier() {
    let valid = true
    const form = document.getElementById('newSupplierForm')

    // add 'is-invalid' class to every element of <form> where there is no value
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
        const supplierData = new FormData(form)

        let json = {}
        supplierData.forEach((value, key) => {
            json[key] = value;
        });

        $(document.getElementById('addSupplierModal')).modal('hide');
        suppliersStore.addSupplier(json);
        form.reset();
    }
}

</script>

<style scoped>
.modal-body .mb-3:last-child {
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
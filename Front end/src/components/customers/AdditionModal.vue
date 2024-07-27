<template>
    <div class="modal fade" id="addCustomerModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t("customers.additionModalTitle") }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="newCustomerForm">
                    <div class="modal-body">
                        <InputField :label="t('customers.formFields.nameLabel')" type="text" name="name" />
                        <InputField :label="t('customers.formFields.contactInfoLabel')" type="text"
                            name="contactInfo" />
                        <InputField :label="t('customers.formFields.additionalLabel')" type="text" name="additional" />
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-success" @click.prevent="validateCustomer()">{{
                        t('general.addBtnText') }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import InputField from '../form_elements/InputField.vue'
import { useCustomersStore } from '@/stores/customers';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

function validateCustomer() {
    let valid = true
    const form = document.getElementById('newCustomerForm')

    // add 'is-invalid' class to every element of <form> that has no value
    for (const element of form.elements) {
        if (element.tagName === 'INPUT' && !element.value && !['additional', 'address'].includes(element.name)) {
            element.classList.add('is-invalid');
            valid = false
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid) {
        const customerData = new FormData(form)

        let json = {}
        customerData.forEach((value, key) => {
            json[key] = value;
        });

        $(document.getElementById('addCustomerModal')).modal('hide');
        useCustomersStore().addCustomer(json);
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
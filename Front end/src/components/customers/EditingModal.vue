<template>
    <div class="modal fade" id="editCustomerModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t("customers.editionModalTitle") }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="editCustomerForm">
                    <div class="modal-body">
                        <InputField :label="t('customers.formFields.nameLabel')" type="text" name="name"
                            :value="oldCustomerData ? oldCustomerData.name : ''" />
                        <InputField :label="t('customers.formFields.contactInfoLabel')" type="text" name="contactInfo"
                            :value="oldCustomerData ? oldCustomerData.contactInfo : ''" />
                        <div class="mb-3">
                            <label class="form-label">{{ t("customers.formFields.addressesLabel") }}</label>
                            <textarea class="form-control" rows="2" style="resize: none;"
                                readonly>{{ oldCustomerData ? `${oldCustomerData.addresses.join(', ')}.` : '' }}</textarea>
                            <div class="form-text">{{ t("customers.formFields.addressesNote") }}
                            </div>
                        </div>
                        <InputField :label="t('customers.formFields.additionalLabel')" type="text" name="additional"
                            :value="oldCustomerData ? oldCustomerData.additional : ''" />
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-success" @click.prevent="validateCustomer()">{{
                        t("general.saveBtnText") }}</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCustomersStore } from '@/stores/customers';
import InputField from '../form_elements/InputField.vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const selectedCustomerId = ref(null);
const oldCustomerData = computed(() => useCustomersStore().customersData.find(customer => customer.id === Number(selectedCustomerId.value)))

onMounted(() => {
    const modalElement = document.getElementById('editCustomerModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        selectedCustomerId.value = btn.parentElement.getAttribute('data-customer-id');
    });
});

function validateCustomer() {
    let valid = true
    const form = document.getElementById('editCustomerForm')

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
        json.id = selectedCustomerId.value;
        customerData.forEach((value, key) => {
            json[key] = value;
        });

        $(document.getElementById('editCustomerModal')).modal('hide');
        useCustomersStore().editCustomer(json);
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
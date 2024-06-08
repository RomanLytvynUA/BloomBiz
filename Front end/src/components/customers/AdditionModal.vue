<template>
    <div class="modal fade" id="addCustomerModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Додати нового клієнта</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="newCustomerForm">
                    <div class="modal-body">
                        <InputField label="Ім'я:" type="text" name="name" />
                        <InputField label="Контакти:" type="text" name="contactInfo" />
                        <InputField label="Адреса:" type="text" name="address" />
                        <InputField label="Додатково:" type="text" name="additional" />
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                        <button type="submit" class="btn btn-primary"
                            @click.prevent="validateCustomer()">Зберегти</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import InputField from '../form_elements/InputField.vue'
import { useCustomersStore } from '@/stores/customers';

function validateCustomer() {
    let valid = true
    const form = document.getElementById('newCustomerForm')

    // add 'is-invalid' class to every element of <form> where there is no value
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
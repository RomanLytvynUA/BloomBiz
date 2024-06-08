<template>
    <div class="modal fade" id="editCustomerModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Змінити постачальника</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="editCustomerForm">
                    <div class="modal-body">
                        <InputField label="Ім'я:" type="text" name="name"
                            :value="oldCustomerData ? oldCustomerData.name : ''" />
                        <InputField label="Контакти:" type="text" name="contactInfo"
                            :value="oldCustomerData ? oldCustomerData.contactInfo : ''" />
                        <InputField label="Адреса:" type="text" name="address"
                            :value="oldCustomerData ? oldCustomerData.address : ''" />
                        <InputField label="Додатково:" type="text" name="additional"
                            :value="oldCustomerData ? oldCustomerData.additional : ''" />
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
import { ref, computed, onMounted } from 'vue'
import { useCustomersStore } from '@/stores/customers';
import InputField from '../form_elements/InputField.vue';

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
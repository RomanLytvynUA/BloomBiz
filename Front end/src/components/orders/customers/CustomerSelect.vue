<template>
    <div class="mb-3">
        <div class="accordion" id="customerSelectAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                        data-bs-target="#customerSelectAccordionBody" data-bs-parent="#customerSelectAccordion">
                        Інформація про клієнта
                    </button>
                </h2>
                <div id="customerSelectAccordionBody" class="accordion-collapse collapse"
                    data-bs-parent="#customerSelectAccordion">
                    <div class="accordion-body">
                        <div class="mb-3">
                            <div class="form-check">
                                <input v-model="guest" class="form-check-input" type="checkbox">
                                <label class="form-check-label">
                                    Створити замовлення без клієнта
                                </label>
                            </div>
                        </div>
                        <div id="customersData" v-if="!guest">
                            <form id="customerForm">
                                <CustomerForm />
                            </form>
                            <div class="mb-3">
                                <div class="form-check">
                                    <input v-model="receiverIsOrderer" class="form-check-input" type="checkbox">
                                    <label class="form-check-label">
                                        Замовник є отримувачем
                                    </label>
                                </div>
                            </div>
                            <form v-if="!receiverIsOrderer" id="receiverForm">
                                <CustomerForm />
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

import CustomerForm from './CustomerForm.vue';

const guest = ref(true)
const receiverIsOrderer = ref(true)

function collectData() {
    if (guest.value === true) {
        $("#customerSelectAccordionBody").collapse('hide');
        receiverIsOrderer.value = true
        return {}
    }

    let valid = true
    const customerForm = document.getElementById('customerForm')
    const receiverForm = document.getElementById('receiverForm')

    for (const element of receiverIsOrderer.value === false ? [...customerForm.elements, ...receiverForm.elements] : [...customerForm.elements]) {
        if (element.tagName !== 'BUTTON' && !element.disabled && !element.value
            && !['additional', 'address'].includes(element.name)) {
            element.classList.add('is-invalid');
            valid = false
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid) {
        let json = { customer: {} }

        const customerData = new FormData(customerForm)
        customerData.forEach((value, key) => {
            json.customer[key] = value;
        });

        if (receiverIsOrderer.value === false) {
            json.receiver = {}
            const receiverData = new FormData(receiverForm)
            receiverData.forEach((value, key) => {
                json.receiver[key] = value;
            });
            receiverForm.reset()
        }

        $("#customerSelectAccordionBody").collapse('hide');
        customerForm.reset()
        guest.value = true
        receiverIsOrderer.value = true

        return json
    }
}
defineExpose({ collectData })
</script>

<style scoped>
.accordion-item .accordion-button:focus {
    outline: none;
    box-shadow: none;
}

.accordion-item .accordion-button:not(.collapsed) {
    background-color: #F8F8F8;
    color: #212529;
}
</style>
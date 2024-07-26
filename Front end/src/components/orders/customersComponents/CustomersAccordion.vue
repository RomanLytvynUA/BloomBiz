<template>
    <div class="mb-3">
        <div class="accordion" :id="'customerSelectAccordion' + accordionIdPrefix">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                        :data-bs-target="'#customerSelectAccordionBody' + accordionIdPrefix"
                        :data-bs-parent="'#customerSelectAccordion' + accordionIdPrefix">
                        {{ t('orders.customerInfoTitle') }}
                    </button>
                </h2>
                <div :id="'customerSelectAccordionBody' + accordionIdPrefix" class="accordion-collapse collapse"
                    :data-bs-parent="'#customerSelectAccordion' + accordionIdPrefix">
                    <div class="accordion-body">
                        <div :class="guest ? '' : 'mb-3'">
                            <div class="form-check">
                                <input v-model="guest" class="form-check-input" type="checkbox">
                                <label class="form-check-label">
                                    {{ t('orders.customerFields.noCustomerText') }}
                                </label>
                            </div>
                        </div>
                        <div id="customersData" v-if="!guest">
                            <form id="customerForm">
                                <CustomerForm ref="customerForm" :showAddressInput="receiverIsOrderer"
                                    :preselectedAddress="preselectedAddress" />
                            </form>
                            <div :class="receiverIsOrderer ? '' : 'mb-3'">
                                <div class=" form-check">
                                    <input v-model="receiverIsOrderer" class="form-check-input" type="checkbox">
                                    <label class="form-check-label">
                                        {{ t('orders.customerFields.ordrerIsReceiverText') }}
                                    </label>
                                </div>
                            </div>
                            <form v-if="!receiverIsOrderer" id="receiverForm">
                                <CustomerForm ref="receiverForm" :showAddressInput="true"
                                    :preselectedAddress="preselectedAddress" />
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, watchEffect } from 'vue';

import CustomerForm from './CustomerForm.vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps(['accordionIdPrefix', 'preselectedAddress'])
const guest = ref(true)
const receiverIsOrderer = ref(true)

const customerForm = ref(null);
const receiverForm = ref(null);

function reset() {
    $(`#customerSelectAccordionBody${props.accordionIdPrefix}`).collapse('hide');
    if (guest.value !== true) {
        $('#customerForm')[0].reset()
    }
    if (receiverIsOrderer.value !== true) {
        $('#receiverForm')[0].reset()
    }
    guest.value = true
    receiverIsOrderer.value = true
}

function updateData(customerId, receiverId) {
    guest.value = customerId ? false : true;
    receiverIsOrderer.value = receiverId !== customerId ? false : true;

    if (!guest.value) {
        // Have to wait untill form is mounted
        if (customerForm.value === null) {
            const stopWatch = watch(customerForm, (value) => {
                if (value) { customerForm.value.preselectCustomer(customerId); stopWatch(); }
            }, { immediate: true });
        } else {
            customerForm.value.preselectCustomer(customerId)
        }
    }
    if (!receiverIsOrderer.value) {
        // Have to wait untill form is mounted
        if (receiverForm.value === null) {
            const stopWatch = watch(receiverForm, (value) => {
                if (value) { receiverForm.value.preselectCustomer(receiverId); stopWatch(); }
            }, { immediate: true });
        } else {
            receiverForm.value.preselectCustomer(receiverId)
        }
    }
}


function collectData() {
    if (guest.value === true) {
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
        }

        return json
    }
}
defineExpose({ collectData, updateData, reset })
</script>

<style scoped>
form {
    margin-left: 10px;
}

.accordion-item .accordion-button:focus {
    outline: none;
    box-shadow: none;
}

.accordion-item .accordion-button:not(.collapsed) {
    background-color: #F8F8F8;
    color: #212529;
}

:deep() #receiverForm .row:last-child>div {
    margin-bottom: 0 !important;
}
</style>
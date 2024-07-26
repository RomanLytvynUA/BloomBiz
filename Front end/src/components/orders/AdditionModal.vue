<template>
    <div class="modal fade" id="addOrderModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog" style="max-width: 600px;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t("orders.additionModalTitle") }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="newOrderForm">
                        <div class="row">
                            <div class="col-sm-6">
                                <InputField ref="dateInput" :label="t('orders.formFields.dateLabel')"
                                    type="datetime-local" name="date" :value="formatISO(new Date()).slice(0, 16)" />
                            </div>
                            <div class="col-sm-6">
                                <SelectField ref="statusInput" :label="t('orders.formFields.statusLabel')" name="status"
                                    :options="statuses" preselectedValue="" />
                            </div>
                        </div>
                    </form>

                    <CustomerSelect ref="customerSelect" accordionIdPrefix="CreateOrder" />

                    <form id="orderElementsForm" class="mb-3">
                        <ElementsAccordion ref="elementsList" @elements-changed="(data) => elements = data"
                            @total-price-changed="(total) => orderTotal = total" />
                    </form>
                    <form id="orderGeneralForm">
                        <div class="mb-3">
                            <label for="floatingTextarea" class="form-label">{{ t('orders.formFields.additionalLabel')
                                }}</label>
                            <textarea class="form-control" name="additional"></textarea>
                        </div>
                        <div class="input-group">
                            <span class="input-group-text">{{ t('orders.formFields.discountLabel')
                                }}</span>
                            <input type="number" name="discount" class="form-control" v-model="orderDiscount">
                            <span class="input-group-text">{{ t('orders.formFields.priceLabel')
                                }}</span>
                            <input ref="orderTotalField" name="price" type="number" class="form-control"
                                :value="orderTotal - orderTotal * (orderDiscount / 100)">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-success" @click.prevent="validateExpense">{{
                        t('general.addBtnText') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { formatISO } from 'date-fns';

import { useOrdersStore } from '@/stores/orders';

import ElementsAccordion from './elementsComponents/ElementsAccordion.vue'
import CustomerSelect from './customersComponents/CustomersAccordion.vue'

import InputField from '../form_elements/InputField.vue'
import SelectField from '../form_elements/SelectField.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps(['statuses'])

const customerSelect = ref(null);
const elementsList = ref(null);
watch(elementsList, () => {
    if (elementsList.value) {
        elementsList.value.setNewData([], { 'null': true })
    }
})

const orderDiscount = ref(0)
const orderTotal = ref(0)
const orderTotalField = ref(null)
const dateInput = ref(null)
const statusInput = ref(null)
const elements = ref(null)

function validateExpense() {
    let valid = true;
    const form = document.getElementById('newOrderForm');
    const generalForm = document.getElementById('orderGeneralForm');
    const elementsForm = document.getElementById('orderElementsForm');
    const customerData = customerSelect.value.collectData();

    // add 'is-invalid' class to every element of <form> where there is no value
    for (const element of [...form.elements, ...elementsForm.elements, ...generalForm.elements]) {
        if (element.tagName !== 'BUTTON' && !element.disabled && !element.value && element.name !== 'additional') {
            element.classList.add('is-invalid');
            valid = false
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid && typeof customerData === "object") {
        const modalElement = document.getElementById('addOrderModal');
        const formData = new FormData(form)
        const generalFormData = new FormData(generalForm)

        let json = customerData;
        json.elements = elements.value
        formData.forEach((value, key) => {
            json[key] = value;
        });
        generalFormData.forEach((value, key) => {
            json[key] = value;
        });

        $(modalElement).modal('hide');

        useOrdersStore().addOrder(json);
        modalElement.addEventListener('hidden.bs.modal', () => {
            orderDiscount.value = 0
            orderTotal.value = 0
            elements.value = null
            dateInput.value.reset();
            statusInput.value.reset();
            customerSelect.value.reset()
            elementsList.value.reset();
        });
    }
}

</script>

<style scoped>
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
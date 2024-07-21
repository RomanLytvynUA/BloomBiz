<template>
    <div class="modal fade" id="editOrderModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog" style="max-width: 600px;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t("orders.editionModalTitle") }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="editOrderForm">
                        <div class="row">
                            <div class="col-sm-6">
                                <InputField ref="dateInput" :label="t('orders.formFields.dateLabel')"
                                    type="datetime-local" name="date" :value="orderDate" />
                            </div>
                            <div class="col-sm-6">
                                <SelectField ref="statusInput" :label="t('orders.formFields.statusLabel')" name="status"
                                    :options="statuses" :preselectedValue="orderData ? orderData.status : null" />
                            </div>
                        </div>
                    </form>
                    <CustomerSelect ref="customerSelect"
                        :preselectedAddress="orderData ? orderData.customer_address : ''"
                        :accordionIdPrefix="'EditOrder' + (orderData ? orderData.id : 0)" />
                    <form id="editOrderElementsForm" class="mb-3">
                        <ElementsAccordion ref="elementsList" @elements-changed="(data) => { elements = data; }"
                            :accordionId="orderData ? orderData.id : ''" @total-price-changed="(total) => {
                        orderTotal = total;
                        orderTotalField.value = orderTotal - orderTotal * (orderDiscount / 100)
                    }" />
                    </form>
                    <form id="editOrderGeneralForm">
                        <div class="mb-3">
                            <label for="floatingTextarea">{{ t('orders.formFields.additionalLabel') }}</label>
                            <textarea :value="orderAdditional" class="form-control" name="additional"></textarea>
                        </div>
                        <div class="input-group">
                            <span class="input-group-text">{{ t('orders.formFields.discountLabel') }}</span>
                            <input type="number" name="discount" class="form-control" v-model="orderDiscount"
                                @input="orderTotalField.value = orderTotal - orderTotal * (orderDiscount / 100)">
                            <span class="input-group-text">{{ t('orders.formFields.priceLabel') }}</span>
                            <input ref="orderTotalField" name="price" type="number" class="form-control">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-success" @click.prevent="validateExpense">{{
                        t('general.saveBtnText') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue';
import { useOrdersStore } from '@/stores/orders';

import ElementsAccordion from './ElementsAccordion.vue'
import CustomerSelect from './customers/CustomerSelect.vue'
import InputField from '../form_elements/InputField.vue'
import SelectField from '../form_elements/SelectField.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps(['statuses'])
const orderId = ref(null)
const orderData = computed(() => {
    const data = orderId ? useOrdersStore().ordersData.find((order) => order.id == orderId.value) : {}
    return data
})

const orderDate = ref(null);
const customerSelect = ref(null);
const elementsList = ref(null);

const orderDiscount = ref(0)
const orderTotal = ref(0)
const orderTotalField = ref(null)
const dateInput = ref(null)
const statusInput = ref(null)
const elements = ref(null)
const orderAdditional = ref(null)

watch(orderData, () => {
    if (orderData.value) {
        elementsList.value.reset()
        orderDate.value = new Date(orderData.value.date).toISOString().slice(0, 16)
        orderTotal.value = orderData.value.price + orderData.value.price * orderData.value.discount / 100 + 1
        orderDiscount.value = orderData.value.discount
        orderAdditional.value = orderData.value.additional
        const prefilledElementsData = { ...orderData.value.elements, null: false };
        elementsList.value.reset()
        elementsList.value.setNewData([].concat(...Object.keys(orderData.value.elements)), prefilledElementsData)

        orderTotalField.value.value = orderData.value.price
    }
})

onMounted(() => {
    const modalElement = document.getElementById('editOrderModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        orderId.value = btn.parentElement.getAttribute('data-order-id');
        customerSelect.value.updateData(orderData.value ? orderData.value.customer : null, orderData.value ? orderData.value.receiver : null);
    });
});

function validateExpense() {
    let valid = true
    const form = document.getElementById('editOrderForm')
    const elementsForm = document.getElementById('editOrderElementsForm')
    const generalForm = document.getElementById('editOrderGeneralForm')
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
        const modalElement = document.getElementById('editOrderModal');
        const formData = new FormData(form)
        const generalFormData = new FormData(generalForm)

        let json = customerData
        json.elements = elements.value ? elements.value : []
        json.order_id = orderId.value
        formData.forEach((value, key) => {
            json[key] = value;
        });
        generalFormData.forEach((value, key) => {
            json[key] = value;
        });

        $(modalElement).modal('hide');
        useOrdersStore().editOrder(json);
        modalElement.addEventListener('hidden.bs.modal', () => {
            orderDiscount.value = 0
            orderTotal.value = 0
            dateInput.value.reset();
            customerSelect.value.reset();
            statusInput.value.reset();
            orderId.value = null;
        }, { once: true });
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
<template>
    <div class="modal fade" id="editOrderModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Змінити замовлення</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="editOrderForm">
                        <InputField ref="dateInput" label="Дата:" type="date" name="date" :value="orderDate" />
                        <SelectField ref="statusInput" label="Статус:" name="status" :options="statuses"
                            :preselectedValue="orderData ? orderData.status : null" />
                    </form>
                    <CustomerSelect ref="customerSelect"
                        :accordionIdPrefix="'EditOrder' + (orderData ? orderData.id : 0)" />
                    <form id="editOrderElementsForm">
                        <ElementsList ref="elementsList" @elements-changed="(data) => { elements = data; }"
                            @total-price-changed="(total) => {
                            orderTotal = total;
                            orderTotalField.value = orderTotal - orderTotal * (orderDiscount / 100)
                        }" />
                    </form>
                    <br>
                    <form id="editOrderGeneralForm">
                        <div class="input-group mb-3">
                            <span class="input-group-text">Знижка:</span>
                            <input type="number" name="discount" class="form-control" v-model="orderDiscount"
                                @input="orderTotalField.value = orderTotal - orderTotal * (orderDiscount / 100)">
                            <span class="input-group-text">Всього:</span>
                            <input ref="orderTotalField" name="price" type="number" class="form-control">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                    <button type="submit" class="btn btn-primary" @click.prevent="validateExpense">Зберегти</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, onMounted, watch, watchEffect } from 'vue';
import { useOrdersStore } from '@/stores/orders';

import ElementsList from './ElementsList.vue'
import CustomerSelect from './customers/CustomerSelect.vue'
import InputField from '../form_elements/InputField.vue'
import SelectField from '../form_elements/SelectField.vue'

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

watch(orderData, () => {
    if (orderData.value) {
        elementsList.value.reset()
        orderDate.value = new Date(orderData.value.date.split('-').reverse().join('-')).toISOString().split('T')[0]
        orderTotal.value = orderData.value.price + orderData.value.price * orderData.value.discount / 100 + 1
        orderDiscount.value = orderData.value.discount
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
            statusInput.value.reset();
            orderId.value = null;
        }, { once: true });
    }
}
</script>
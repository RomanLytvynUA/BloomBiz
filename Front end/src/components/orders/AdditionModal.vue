<template>
    <div class="modal fade" id="addOrderModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Додати нове замовлення</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="newOrderForm">
                        <InputField ref="dateInput" label="Дата:" type="date" name="date" :value="todaysDate" />
                        <SelectField ref="statusInput" label="Статус:" name="status" :options="orderStatuses"
                            :preselectedValue="'Вітрина'" />
                    </form>

                    <form id="orderElementsForm">
                        <ElementsList ref="elementsList" @elements-changed="(data) => elements = data"
                            @total-price-changed="(total) => orderTotal = total" />
                    </form>
                    <br>
                    <form id="orderGeneralForm">
                        <div class="input-group mb-3">
                            <span class="input-group-text">Знижка:</span>
                            <input type="number" name="discount" class="form-control" v-model="orderDiscount">
                            <span class="input-group-text">Всього:</span>
                            <input ref="orderTotalField" name="price" type="number" class="form-control"
                                :value="orderTotal - orderTotal * (orderDiscount / 100)">
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
import { computed, ref, onMounted, watch } from 'vue';
import { orderStatuses } from '../../config';

import { useOrdersStore } from '@/stores/orders';

import ElementsList from './ElementsList.vue'
import InputField from '../form_elements/InputField.vue'
import SelectField from '../form_elements/SelectField.vue'

const todaysDate = new Date().toISOString().split('T')[0];
const elementsList = ref(null)
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
    let valid = true
    const form = document.getElementById('newOrderForm')
    const generalForm = document.getElementById('orderGeneralForm')
    const elementsForm = document.getElementById('orderElementsForm')

    // add 'is-invalid' class to every element of <form> where there is no value
    for (const element of [...form.elements, ...elementsForm.elements, ...generalForm.elements]) {
        if (element.tagName !== 'BUTTON' && !element.disabled && !element.value && element.name !== 'additional') {
            element.classList.add('is-invalid');
            valid = false
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid) {
        const modalElement = document.getElementById('addOrderModal');
        const formData = new FormData(form)
        const generalFormData = new FormData(generalForm)

        let json = {}
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
            elementsList.value.reset()
        });
    }
}

</script>
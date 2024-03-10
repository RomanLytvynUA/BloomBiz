<template>
    <div class="modal fade" id="addExpenseModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Додати нову витрату</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="newExpenseForm">
                        <InputField ref=dateInput label="Дата:" type="date" name="date" :value="todaysDate" />
                        <CategoriesInput ref="categoryInput" @categoryChanged="(newValue) => selectedCategoryField = newValue" />
                        <SelectField ref="supplierInput" label="Постачальник: " name="supplier" :options="suppliersData" customOptionValue="+ Додати нового" />
                        
                    </form>
                    <form id="expenseElementsForm">
                        <ElementsTable ref="elements" :rows="[]" :category="selectedCategoryField" />
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

import { useExpensesStore } from '@/stores/expenses';
import { useSuppliersStore } from '@/stores/suppliers';

import InputField from '../form_elements/InputField.vue'
import CategoriesInput from '../form_elements/CategoriesInput.vue'
import SelectField from '../form_elements/SelectField.vue'
import ElementsTable from './ElementsTable.vue'

const todaysDate = new Date().toISOString().split('T')[0];
const suppliersData = computed(() => useSuppliersStore().suppliersNames)

const selectedCategoryField = ref(null);

const dateInput = ref(null)
const categoryInput = ref(null)
const supplierInput = ref(null)
const elements = ref(null)

function validateExpense() {
    let valid = true
    const form = document.getElementById('newExpenseForm')
    const elementsForm = document.getElementById('expenseElementsForm')

    // add 'is-invalid' class to every element of <form> where there is no value
    for (const element of [...form.elements, ...elementsForm.elements]) {
        if (element.tagName !== 'BUTTON' && !element.disabled && !element.value && element.name !== 'additional') {
            element.classList.add('is-invalid');
            valid = false
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid) {
        const modalElement = document.getElementById('addExpenseModal');
        const supplierData = new FormData(form)

        let json = {}
        json.elements = elements.value.rows.map(({ options, ...rest }) => rest)
        json.total = elements.value.totalPrice
        supplierData.forEach((value, key) => {
            json[key] = value;
        });
        
        $(modalElement).modal('hide');
        useExpensesStore().addExpense(json);

        modalElement.addEventListener('hidden.bs.modal', (event) => {
            dateInput.value.reset();
            categoryInput.value.reset();
            supplierInput.value.reset();
            elements.value.rows = []
            elements.value.totalPrice = 0
        });
    }
}

</script>
<template>
    <div class="modal fade" id="addExpenseModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog" style="max-width: 600px;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('expenses.additionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- Expense fields -->
                    <form id="newExpenseForm">
                        <InputField ref=dateInput :label="t('expenses.formFields.dateLabel')" type="date" name="date"
                            :value="todaysDate" />
                        <div class="row">
                            <div class="col-sm-6">
                                <CategoriesInput ref="categoryInput" :label="t('expenses.formFields.categoryLabel')"
                                    @categoryChanged="(newValue) => selectedCategory = newValue" />
                            </div>
                            <div class="col-sm-6">
                                <SelectField ref="supplierInput" :label="t('expenses.formFields.supplierLabel')"
                                    name="supplier"
                                    :options="suppliersNames.filter((supplier) => suppliersToIgnore ? !suppliersToIgnore.includes(supplier) : true)"
                                    :customOptionValue="t('general.customOptions.customSupplierText')" />
                            </div>
                        </div>
                    </form>
                    <!-- Expense elements fields -->
                    <form id="expenseElementsForm">
                        <ElementsTable ref="elements" style="margin-bottom: 0;" :rows="[]"
                            :category="selectedCategory" />
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
import { computed, ref } from 'vue';

import { useExpensesStore } from '@/stores/expenses';
import { useSuppliersStore } from '@/stores/suppliers';
import { useSettingsStore } from '@/stores/settings';

import InputField from '../form_elements/InputField.vue'
import CategoriesInput from '../form_elements/CategoriesInput.vue'
import SelectField from '../form_elements/SelectField.vue'

import ElementsTable from './elementsComponents/ElementsTable.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const todaysDate = new Date().toISOString().split('T')[0];
const suppliersNames = computed(() => useSuppliersStore().suppliersNames)
const suppliersToIgnore = computed(() => useSettingsStore().settingsData.expensesSuppliersToIgnore)

const selectedCategory = ref(null);

const dateInput = ref(null)
const categoryInput = ref(null)
const supplierInput = ref(null)
const elements = ref(null)

function validateExpense() {
    let valid = true
    const form = document.getElementById('newExpenseForm')
    const elementsForm = document.getElementById('expenseElementsForm')

    // add 'is-invalid' class to every element of <form> that has no value
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
        const expenseData = new FormData(form)

        let json = {}
        json.elements = elements.value.rows.map(({ options, ...rest }) => rest)
        json.total = elements.value.totalPrice
        expenseData.forEach((value, key) => {
            json[key] = value;
        });

        useExpensesStore().addExpense(json);
        $(modalElement).modal('hide');

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
<template>
    <div class="modal fade" id="editExpenseModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog" style="max-width: 600px;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('expenses.editionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="editExpenseForm">
                        <InputField ref="dateInput" :label="t('expenses.formFields.dateLabel')" type="date" name="date"
                            :value="expenseData ? new Date(expenseData.date.split('-').reverse().join('-')).toISOString().split('T')[0] : null" />
                        <div class="row">
                            <div class="col-sm-6">
                                <CategoriesInput ref="categoryInput" :label="t('expenses.formFields.categoryLabel')"
                                    :constant="categoryData ? { category: categoryData.name, units: categoryData.units } : {}" />
                            </div>
                            <div class="col-sm-6">
                                <SelectField ref="supplierInput" :label="t('expenses.formFields.supplierLabel')"
                                    name="supplier"
                                    :options="suppliersNames.filter((supplier) => suppliersToIgnore ? !suppliersToIgnore.includes(supplier) : true)"
                                    :preselectedValue="supplierData ? supplierData.name : null"
                                    :customOptionValue="t('general.customOptions.customSupplierText')" />
                            </div>
                        </div>
                    </form>
                    <form id="editExpenseElementsForm">
                        <ElementsTable ref="elements" style="margin-bottom: 0;" :rows="[]"
                            :category="categoryData ? categoryData.name : null" />
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

import { useExpensesStore } from '@/stores/expenses';
import { useSuppliersStore } from '@/stores/suppliers';
import { useGoodsStore } from '../../stores/goods';
import { useSettingsStore } from '@/stores/settings';

import InputField from '../form_elements/InputField.vue'
import CategoriesInput from '../form_elements/CategoriesInput.vue'
import SelectField from '../form_elements/SelectField.vue'

import ElementsTable from './elementsComponents/ElementsTable.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const expenseData = computed(() => useExpensesStore().expensesData.find((expense) => expense.id == selectedExpenseId.value))
const suppliersNames = computed(() => useSuppliersStore().suppliersNames)
const suppliersToIgnore = computed(() => useSettingsStore().settingsData.expensesSuppliersToIgnore)
const supplierData = computed(() => expenseData.value ? useSuppliersStore().suppliersData.find((supplier) => supplier.id === expenseData.value.supplier) : null)
const categoryData = computed(() => expenseData.value ? useGoodsStore().goodsData.find((category) => category.id == expenseData.value.category) : null)

const dateInput = ref(null)
const supplierInput = ref(null)
const elements = ref(null)

const selectedExpenseId = ref(null);
onMounted(() => {
    const modalElement = document.getElementById('editExpenseModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        selectedExpenseId.value = btn.parentElement.getAttribute('data-expense-id');
    });
});

watch(expenseData, () => {
    if (expenseData.value) {
        elements.value.reset()
        elements.value.totalPrice = expenseData.value.total

        for (const element of expenseData.value.elements) {
            const elementData = useGoodsStore().minGoodsData.find((product) => product.id === element.product)
            elements.value.addRow(categoryData.value.name, elementData ? elementData.name : "-",
                element.quantity, element.price);
        }
    }
})


function validateExpense() {
    let valid = true
    const form = document.getElementById('editExpenseForm')
    const elementsForm = document.getElementById('editExpenseElementsForm')

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
        const modalElement = document.getElementById('editExpenseModal');
        const supplierData = new FormData(form)

        let json = {}
        json.elements = elements.value.rows.map(({ options, ...rest }) => rest)
        json.total = elements.value.totalPrice
        json.expense_id = selectedExpenseId.value
        supplierData.forEach((value, key) => {
            json[key] = value;
        });

        supplierInput.value.reset()
        $(modalElement).modal('hide');
        useExpensesStore().editExpense(json);
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
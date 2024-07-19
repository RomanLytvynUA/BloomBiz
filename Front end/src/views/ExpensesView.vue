<template>
  <Headline :title="t('expenses.title')" :description="t('expenses.description')" />
  <div class="text-center">
    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addExpenseModal">{{
    t('general.addBtnText')
  }}</button> <br>
  </div>
  <br>

  <TableComponent ref="tableComponent" :loading="loading" @filterChanged="filterExpenses" :filters="tableFilters"
    :headers="tableHeaders" :rows="tableRows" />

  <AdditionModal />
  <EditingModal />
  <DeletionModal />
</template>

<script setup>
import { ref, computed, markRaw, watch, onMounted } from 'vue'
import { useExpensesStore } from '../stores/expenses';
import { useSuppliersStore } from '../stores/suppliers';
import { useGoodsStore } from '../stores/goods';
import { useSettingsStore } from '../stores/settings';

import Headline from '../components/Headline.vue'

import TableComponent from '../components/table_elements/TableComponent.vue';
import ActionButtons from '../components/table_elements/ActionButtons.vue';
import DateFilter from '../components/table_elements/filters/DateFilter.vue';
import SelectFilter from '../components/table_elements/filters/SelectFilter.vue';

import AdditionModal from '../components/expenses/AdditionModal.vue';
import EditingModal from '../components/expenses/EditingModal.vue';
import DeletionModal from '../components/expenses/DeletionModal.vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const expensesStorage = useExpensesStore();
const suppliersStorage = useSuppliersStore();
const goodsStorage = useGoodsStore();

// get and filter the expenses
const loading = computed(() => useExpensesStore().inLoadingState);
const safetyMode = computed(() => useSettingsStore().settingsData.expensesSafetyMode === "true" ? true : false);
const expensesData = computed(() => expensesStorage.expensesData)
const suppliersData = computed(() => suppliersStorage.suppliersNames)
const categoriesData = computed(() => goodsStorage.categoriesNames)
const filteredExpenses = ref([])

function filterExpenses() {
  if (tableComponent.value) {
    const dateFilterComponent = tableComponent.value.$refs.dateFilterComponent[0]
    const supplierFilterComponent = tableComponent.value.$refs.supplierFilterComponent[0]
    const categoryFilterComponent = tableComponent.value.$refs.categoryFilterComponent[0]

    filteredExpenses.value = expensesData.value.filter(expense => {
      return dateFilterComponent.filterDate(expense.date) &&
        supplierFilterComponent.filterData(suppliersStorage.suppliersData.find(supplier => supplier.id == expense.supplier)?.name) &&
        categoryFilterComponent.filterData(goodsStorage.goodsData.find(category => category.id == expense.category)?.name)
    })
  }
}

watch(() => expensesData.value, filterExpenses, { deep: true })

// table staff
const tableComponent = ref(null);

const tableFilters = ref([
  { component: markRaw(DateFilter), reference: 'dateFilterComponent' },
  { component: markRaw(SelectFilter), reference: 'supplierFilterComponent', props: { options: suppliersData } },
  { component: markRaw(SelectFilter), reference: 'categoryFilterComponent', props: { options: categoriesData } },
])

const tableHeaders = ref([
  { 'name': computed(() => t('expenses.tableHeaders.date')), 'size': '30%' },
  { 'name': computed(() => t('expenses.tableHeaders.supplier')), 'size': '20%' },
  { 'name': computed(() => t('expenses.tableHeaders.category')), 'size': '15%' },
  { 'name': computed(() => t('expenses.tableHeaders.price')), 'size': '15%' },
  { 'name': computed(() => t('expenses.tableHeaders.action')), 'size': '20%' },
]);

const tableRows = computed(() => filteredExpenses.value.map(expense => [
  new Date(expense.date).toLocaleDateString('en-GB').split('/').join('-'),
  suppliersStorage.suppliersData.find(supplier => supplier.id == expense.supplier)?.name,
  goodsStorage.goodsData.find(category => category.id == expense.category)?.name,
  expense.total,
  {
    component: ActionButtons,
    props: {
      delModalId: "#delExpenseModal",
      editModalId: "#editExpenseModal",
      'data-expense-id': expense.id,
      delDisabled: safetyMode.value,
    },
  }
]));

onMounted(() => {
  filterExpenses()

})
</script>

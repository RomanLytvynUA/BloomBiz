<template>
  <Headline title="Витрати"
    description="Тут ви можете зареєструвати та переглянути свої витрати. При додаванні постачання, нові товари будуть додані до вашого складу." />
  <div class="text-center">
    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addExpenseModal">Додати</button> <br>
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
  // console.log(categoriesData.value)
  if (tableComponent.value) {
    const dateFilterComponent = tableComponent.value.$refs.dateFilterComponent[0]
    const supplierFilterComponent = tableComponent.value.$refs.supplierFilterComponent[0]
    const categoryFilterComponent = tableComponent.value.$refs.categoryFilterComponent[0]

    filteredExpenses.value = expensesData.value.filter(expense => {
      return dateFilterComponent.filterDate(expense.date) &&
        supplierFilterComponent.filterData(suppliersStorage.suppliersData.find(supplier => supplier.id == expense.supplier).name) &&
        categoryFilterComponent.filterData(goodsStorage.goodsData.find(category => category.id == expense.category).name)
    })
  }
}

watch(expensesData, filterExpenses)
// watch(categoriesData, console.log(categoriesData))

// table staff
const tableComponent = ref(null);

const tableFilters = ref([
  { component: markRaw(DateFilter), reference: 'dateFilterComponent' },
  { component: markRaw(SelectFilter), reference: 'supplierFilterComponent', props: { options: suppliersData } },
  { component: markRaw(SelectFilter), reference: 'categoryFilterComponent', props: { options: categoriesData } },
])

const tableHeaders = ref([
  { 'name': 'Дата', 'size': '300px' },
  { 'name': 'Постачальник', 'size': '170px' },
  { 'name': 'Категорія', 'size': '170px' },
  { 'name': 'Ціна', 'size': '120px' },
  { 'name': 'Дія', 'size': '190px' },
]);

const tableRows = computed(() => filteredExpenses.value.map(expense => [
  new Date(expense.date).toLocaleDateString('en-GB').split('/').join('-'),
  suppliersStorage.suppliersData.find(supplier => supplier.id == expense.supplier).name,
  goodsStorage.goodsData.find(category => category.id == expense.category).name,
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

<template>
  <Headline title="Замовлення" description="Тут ви можете додавати замовлення своїх клієнтів та редагувати їх." />
  <div class="text-center">
    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addOrderModal">Додати</button> <br>
  </div>
  <br>
  <TableComponent ref="tableComponent" :loading="loading" @filterChanged="filteringState = true; filterOrders()"
    :filters="tableFilters" :headers="tableHeaders" :rows="tableRows" />

  <AdditionModal :statuses="ordersStatuses" />
  <EditingModal :statuses="ordersStatuses" />
  <DeletionModal />

</template>

<script setup>
import { ref, computed, markRaw, watch, onMounted } from 'vue'
import { useOrdersStore } from '../stores/orders';
import { useGoodsStore } from '../stores/goods';
import { useSettingsStore } from '../stores/settings';

import Headline from '../components/Headline.vue'

import TableComponent from '../components/table_elements/TableComponent.vue';
import ActionButtons from '../components/table_elements/ActionButtons.vue';
import DateFilter from '../components/table_elements/filters/DateFilter.vue';
import SelectFilter from '../components/table_elements/filters/SelectFilter.vue';
import Popover from '../components/table_elements/Popover.vue';

import AdditionModal from '../components/orders/AdditionModal.vue';
import EditingModal from '../components/orders/EditingModal.vue';
import DeletionModal from '../components/orders/DeletionModal.vue';

const ordersStorage = useOrdersStore();
const loading = computed(() => useOrdersStore().inLoadingState);

// get and filter the expenses
const ordersData = computed(() => ordersStorage.ordersData)
const filteredOrders = ref([])
const safetyMode = computed(() => useSettingsStore().settingsData.ordersSafetyMode === "true" ? true : false);
const ordersStatuses = computed(() => useSettingsStore().settingsData.ordersStatuses);

function filterOrders() {
  if (tableComponent.value) {
    const dateFilterComponent = tableComponent.value.$refs.dateFilterComponent[0]
    const statusFilterComponent = tableComponent.value.$refs.statusFilterComponent[0]
    const filteredData = ordersData.value.filter(order => {
      return dateFilterComponent.filterDate(order.date) &&
        statusFilterComponent.filterData(order.status)
    })
    filteredOrders.value = filteredData
  }
}
watch(ordersData, filterOrders)

// table staff
const tableComponent = ref(null);

const tableFilters = ref([
  { component: markRaw(DateFilter), reference: 'dateFilterComponent' },
  { component: markRaw(SelectFilter), reference: 'statusFilterComponent', props: { options: ordersStatuses } },
])

const tableHeaders = ref([
  { 'name': 'Дата', 'size': '300px' },
  { 'name': 'Статус', 'size': '125px' },
  { 'name': 'Склад', 'size': '200px' },
  { 'name': 'Ціна', 'size': '125px' },
  { 'name': 'Дія', 'size': '180px' },
]);

const tableRows = computed(() => filteredOrders.value.map(order => [
  new Date(order.date).toLocaleDateString('en-GB').split('/').join('-'),
  order.status,
  {
    component: Popover,
    props: {
      maxSize: 20,
      text: `${[].concat(...Object.values(order.elements)).map(element => useGoodsStore().minGoodsData.find(product => product.id == element.product).name).join(', ')}.`,
      title: 'Склад замовлення:',
      id: order.id,
    },
  },
  order.price,
  {
    component: ActionButtons,
    props: {
      delModalId: "#delOrderModal",
      delText: "Розібрати",
      editModalId: "#editOrderModal",
      'data-order-id': order.id,
      delDisabled: safetyMode.value,
    },
  }
]));

onMounted(() => {
  filterOrders()
})
</script>
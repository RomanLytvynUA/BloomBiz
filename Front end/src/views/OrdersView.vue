<template>
  <Headline :title="t('orders.title')" :description="t('orders.description')" />
  <div class="text-center">
    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addOrderModal">{{ t('general.addBtnText')
      }}</button> <br>
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

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

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
watch(() => ordersData.value, () => filterOrders(), { deep: true })

// table staff
const tableComponent = ref(null);

const tableFilters = ref([
  { component: markRaw(DateFilter), reference: 'dateFilterComponent' },
  { component: markRaw(SelectFilter), reference: 'statusFilterComponent', props: { options: ordersStatuses } },
])

const tableHeaders = ref([
  { 'name': computed(() => t("orders.tableHeaders.date")), 'size': '25%' },
  { 'name': computed(() => t("orders.tableHeaders.status")), 'size': '15%' },
  { 'name': computed(() => t("orders.tableHeaders.composition")), 'size': '30%' },
  { 'name': computed(() => t("orders.tableHeaders.price")), 'size': '10%' },
  { 'name': computed(() => t("orders.tableHeaders.action")), 'size': '20%' },
]);

const tableRows = computed(() => filteredOrders.value.map(order => {
  return [
    new Date(order.date).toLocaleDateString('en-GB').split('/').join('-'),
    order.status,
    {
      component: Popover,
      props: {
        maxSize: 20,
        text: `${[].concat(...Object.values(order.elements)).map(element => {
          const productData = useGoodsStore().minGoodsData.find(product => product.id == element.product)
          return productData ? productData.name : ''
        }).join(', ')}.`,
        title: t("orders.compositionPopupTitle"),
        id: order.id,
      },
    },
    order.price,
    {
      component: ActionButtons,
      props: {
        delModalId: "#delOrderModal",
        delText: t("orders.delBtnText"),
        editModalId: "#editOrderModal",
        'data-order-id': order.id,
        delDisabled: safetyMode.value,
      },
    }
  ]
}));

onMounted(() => {
  filterOrders()
})
</script>
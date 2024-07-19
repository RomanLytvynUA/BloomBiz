<template>
  <Headline :title="t('suppliers.title')" :description="t('suppliers.description')" />
  <div class="text-center">
    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addSupplierModal">{{
    t('general.addBtnText')
  }}</button>
  </div>
  <br>

  <TableComponent ref="tableComponent" :filters="tableFilters" :headers="tableHeaders" :loading="loading"
    :rows="tableRows" />

  <AdditionModal />
  <EditingModal />
  <DeletionModal />
</template>

<script setup>
import { ref, computed, markRaw } from 'vue';
import { useSuppliersStore } from '@/stores/suppliers';
import { useSettingsStore } from '@/stores/settings';

import Headline from '../components/Headline.vue';
import TableComponent from '../components/table_elements/TableComponent.vue';
import ActionButtons from '../components/table_elements/ActionButtons.vue';
import AdditionModal from '../components/suppliers/AdditionModal.vue';
import EditingModal from '../components/suppliers/EditingModal.vue';
import DeletionModal from '../components/suppliers/DeletionModal.vue';
import InputFilter from '../components/table_elements/filters/InputFilter.vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const tableComponent = ref(null)
const loading = computed(() => useSuppliersStore().inLoadingState);

const suppliersStore = useSuppliersStore();
const safetyMode = computed(() => useSettingsStore().settingsData.suppliersSafetyMode === "true" ? true : false);
const suppliers = computed(() => suppliersStore.suppliersData);

const filteredSuppliers = computed(() => {
  const filteredData = tableComponent.value ? suppliers.value.filter(supplier => {
    const nameFilterComponent = tableComponent.value.$refs.nameFilterComponent[0];
    const contactsFilterComponent = tableComponent.value.$refs.contactsFilterComponent[0];

    return nameFilterComponent.filterData(supplier.name) && contactsFilterComponent.filterData(supplier.contactInfo)
  }) : []
  return filteredData
})

const tableFilters = ref([
  {
    component: markRaw(InputFilter),
    reference: 'nameFilterComponent',
    props: { placeholder: computed(() => t('suppliers.filtersPlaceholders.enterName')) }
  },
  {
    component: markRaw(InputFilter),
    reference: 'contactsFilterComponent',
    props: { placeholder: computed(() => t('suppliers.filtersPlaceholders.enterContactInfo')) }
  },
]);

const tableHeaders = ref([
  { 'name': computed(() => t('suppliers.tableHeaders.name')), 'size': '20%' },
  { 'name': computed(() => t('suppliers.tableHeaders.contactInfo')), 'size': '30%' },
  { 'name': computed(() => t('suppliers.tableHeaders.additional')), 'size': '30%' },
  { 'name': computed(() => t('suppliers.tableHeaders.action')), 'size': '20%' },
]);

const tableRows = computed(() => filteredSuppliers.value.map(supplier => [
  supplier.name,
  supplier.contactInfo,
  supplier.additional,
  {
    component: ActionButtons,
    props: {
      delModalId: "#delSupplierModal",
      editModalId: "#editSupplierModal",
      'data-supplier-id': supplier.id,
      delDisabled: safetyMode.value,
    },
  }
]));

</script>
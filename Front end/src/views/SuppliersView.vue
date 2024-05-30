<template>
  <Headline title="Постачальники"
    description="Тут ви можете продивлятись, редагувати та додавати нових постачальників." />
  <div class="text-center">
    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addSupplierModal">Додати</button>
  </div>
  <br>

  <TableComponent :headers="tableHeaders" :rows="tableRows" />

  <AdditionModal />
  <EditingModal />
  <DeletionModal />
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useSuppliersStore } from '@/stores/suppliers';
import { useSettingsStore } from '@/stores/settings';

import Headline from '../components/Headline.vue';
import TableComponent from '../components/table_elements/TableComponent.vue';
import ActionButtons from '../components/table_elements/ActionButtons.vue';
import AdditionModal from '../components/suppliers/AdditionModal.vue';
import EditingModal from '../components/suppliers/EditingModal.vue';
import DeletionModal from '../components/suppliers/DeletionModal.vue';

// get the suppliers
const suppliersStore = useSuppliersStore();
const safetyMode = computed(() => useSettingsStore().settingsData.suppliersSafetyMode === "true" ? true : false);
const suppliers = computed(() => suppliersStore.suppliersData);
const tableHeaders = ref([
  { 'name': 'Ім\'я', 'size': '150px' },
  { 'name': 'Контакти', 'size': '290px' },
  { 'name': 'Додатково', 'size': '260px' },
  { 'name': 'Дія', 'size': '250px' },
]);

const tableRows = computed(() => suppliers.value.map(supplier => [
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
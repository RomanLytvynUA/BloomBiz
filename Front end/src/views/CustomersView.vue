<template>
    <Headline title="Клієнти" description="Тут ви можете переглянути, видалити та додати клієнтів." />

    <div class="text-center">
        <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addCustomerModal">Додати</button>
    </div>
    <br>

    <TableComponent ref="tableComponent" :rows="tableRows" :headers="tableHeaders" :filters="tableFilters" />

    <AdditionModal />
    <EditingModal />
    <DeletionModal />
</template>

<script setup>
import { ref, computed, markRaw } from 'vue';

import { useCustomersStore } from '../stores/customers';

import Headline from '../components/Headline.vue'

import AdditionModal from '../components/customers/AdditionModal.vue';
import EditingModal from '../components/customers/EditingModal.vue';
import DeletionModal from '../components/customers/DeletionModal.vue';

import InputFilter from '../components/table_elements/filters/InputFilter.vue';
import TableComponent from '../components/table_elements/TableComponent.vue';
import ActionButtons from '../components/table_elements/ActionButtons.vue';

const customersData = computed(() => tableComponent.value ? useCustomersStore().customersData.filter(customer => {
    const nameFilterComponent = tableComponent.value.$refs.nameFilterComponent[0];
    const contactsFilterComponent = tableComponent.value.$refs.contactsFilterComponent[0];
    const addressFilterComponent = tableComponent.value.$refs.addressFilterComponent[0];

    return nameFilterComponent.filterData(customer.name) && contactsFilterComponent.filterData(customer.contactInfo)
        && addressFilterComponent.filterData(customer.address)
}) : [])

const tableComponent = ref(null)
const tableHeaders = ref([
    { 'name': 'Ім\'я', 'size': '15%' },
    { 'name': 'Контакти', 'size': '20%' },
    { 'name': 'Адреса', 'size': '25%' },
    // { 'name': 'Додатково', 'size': '25%' },
    { 'name': 'Дія', 'size': '20%' },
]);

const tableFilters = ref([
    { component: markRaw(InputFilter), reference: 'nameFilterComponent', props: { placeholder: 'Введіть ім\'я...' } },
    { component: markRaw(InputFilter), reference: 'contactsFilterComponent', props: { placeholder: 'Введіть контакти...' } },
    { component: markRaw(InputFilter), reference: 'addressFilterComponent', props: { placeholder: 'Введіть адресу...' } },
])

const tableRows = computed(() => customersData.value.map(customer => [
    customer.name,
    customer.contactInfo,
    customer.address,
    // customer.additional,
    {
        component: ActionButtons,
        props: {
            delModalId: "#delCustomerModal",
            editModalId: "#editCustomerModal",
            'data-customer-id': customer.id,
            //   delDisabled: safetyMode.value,
        },
    }
]));
</script>
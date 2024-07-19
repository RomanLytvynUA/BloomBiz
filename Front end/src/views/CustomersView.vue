<template>
    <Headline :title="t('customers.title')" :description="t('customers.description')" />
    <div class="text-center">
        <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addCustomerModal">{{
        t('general.addBtnText')
    }}</button>
    </div>
    <br>

    <TableComponent ref="tableComponent" :loading="loading" :rows="tableRows" :headers="tableHeaders"
        :filters="tableFilters" />

    <AdditionModal />
    <EditingModal />
    <DeletionModal />
</template>

<script setup>
import { ref, computed, markRaw } from 'vue';

import { useCustomersStore } from '../stores/customers';
import { useSettingsStore } from '../stores/settings';

import Headline from '../components/Headline.vue'

import AdditionModal from '../components/customers/AdditionModal.vue';
import EditingModal from '../components/customers/EditingModal.vue';
import DeletionModal from '../components/customers/DeletionModal.vue';

import InputFilter from '../components/table_elements/filters/InputFilter.vue';
import TableComponent from '../components/table_elements/TableComponent.vue';
import ActionButtons from '../components/table_elements/ActionButtons.vue';
import Popover from '../components/table_elements/Popover.vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const loading = computed(() => useCustomersStore().inLoadingState);

const safetyMode = computed(() => useSettingsStore().settingsData.customersSafetyMode === "true" ? true : false);
const customersData = computed(() => tableComponent.value && !loading.value ? useCustomersStore().customersData.filter(customer => {
    const nameFilterComponent = tableComponent.value.$refs.nameFilterComponent[0];
    const contactsFilterComponent = tableComponent.value.$refs.contactsFilterComponent[0];
    const addressFilterComponent = tableComponent.value.$refs.addressFilterComponent[0];

    return nameFilterComponent.filterData(customer.name) && contactsFilterComponent.filterData(customer.contactInfo)
        && addressFilterComponent.filterData(customer.addresses.join(' '))
}) : [])

const tableComponent = ref(null)
const tableHeaders = ref([
    { 'name': computed(() => t('customers.tableHeaders.name')), 'size': '20%' },
    { 'name': computed(() => t('customers.tableHeaders.contactInfo')), 'size': '30%' },
    { 'name': computed(() => t('customers.tableHeaders.address')), 'size': '30%' },
    { 'name': computed(() => t('customers.tableHeaders.action')), 'size': '20%' },
]);

const tableFilters = ref([
    {
        component: markRaw(InputFilter),
        reference: 'nameFilterComponent',
        props: { placeholder: computed(() => t('customers.filtersPlaceholders.enterName')) }
    },
    {
        component: markRaw(InputFilter),
        reference: 'contactsFilterComponent',
        props: { placeholder: computed(() => t('customers.filtersPlaceholders.enterContactInfo')) }
    },
    {
        component: markRaw(InputFilter),
        reference: 'addressFilterComponent',
        props: { placeholder: computed(() => t('customers.filtersPlaceholders.enterAddress')) }
    },
]);

const tableRows = computed(() => customersData.value.map(customer => [
    customer.name,
    customer.contactInfo,
    (
        customer.addresses.length ?
            {
                component: Popover,
                props: {
                    maxSize: 30,
                    text: `${customer.addresses.join('/')}.`,
                    title: t('customers.addressesPopoverTitle'),
                    id: `customerAddressesPopover${customer.id}`,
                }
            } : ''),
    {
        component: ActionButtons,
        props: {
            delModalId: "#delCustomerModal",
            editModalId: "#editCustomerModal",
            'data-customer-id': customer.id,
            delDisabled: safetyMode.value,
        },
    }
]));
</script>
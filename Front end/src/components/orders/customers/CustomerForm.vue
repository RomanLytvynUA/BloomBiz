<template>
    <div class="row">
        <Autocomplete divClasses="col-md-6 mb-3" :label="t('orders.customerFields.nameLabel')" name="name"
            :forceCustomInput="newCustomer" :options="filteredCustomersData.map((customer) => customer.name)"
            :customOptionLabel="t('general.customOptions.customCustomerText')"
            :preselectedValue="selectedCustomerData ? selectedCustomerData.name : ''"
            @customOptionSelected="() => { newCustomer = true; selectedCustomerData = null }"
            @valueSelected="(option) => !newCustomer ? selectedCustomerData = customersData.find(customer => customer.name === option) : {}" />
        <Autocomplete divClasses="col-md-6 mb-3" :label="t('orders.customerFields.contactInfoLabel')" name="contactInfo"
            :forceCustomInput="newCustomer" :options="filteredCustomersData.map((customer) => customer.contactInfo)"
            :customOptionLabel="t('general.customOptions.customCustomerText')"
            :preselectedValue="selectedCustomerData ? selectedCustomerData.contactInfo : ''"
            @customOptionSelected="() => { newCustomer = true; selectedCustomerData = null }"
            @valueSelected="(option) => !newCustomer ? selectedCustomerData = customersData.find(customer => customer.contactInfo === option) : {}" />
    </div>
    <div class="row" v-if="showAddressInput">
        <div class="mb-3">
            <div class="form-check form-check-inline">
                <input v-model="pickup" class="form-check-input" type="checkbox" id="pickupCheckbox">
                <label class="form-check-label" for="pickupCheckbox">{{ t('orders.customerFields.pickupText') }}</label>
            </div>
            <Autocomplete v-if="!pickup" divClasses="col-md-12" :label="t('orders.customerFields.addressLabel')"
                name="address" :disabled="!Boolean(selectedCustomerData) && !newCustomer"
                :forceCustomInput="newCustomer" :options="selectedCustomerData ? selectedCustomerData.addresses : []"
                :customOptionLabel="t('general.customOptions.customAddressText')"
                :preselectedValue="preselectedAddress" />
        </div>
    </div>
    <div class="row">
        <div class="col-md-12 mb-3">
            <label for="customerAddinional">{{ t('orders.customerFields.additionalLabel') }}</label>
            <input v-model="additionalField" type="text" class="form-control" name="additional" id="customerAddinional"
                :disabled="!newCustomer">
        </div>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useCustomersStore } from '../../../stores/customers';
import { useSettingsStore } from '@/stores/settings';

import Autocomplete from '@/components/form_elements/Autocomplete.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps(['showAddressInput', 'preselectedAddress'])

const customersData = computed(() => useCustomersStore().customersData)
const filteredCustomersData = computed(() => customersData.value.filter(customer => !useSettingsStore().settingsData.ordersCustomersToIgnore.includes(customer.contactInfo)))

const additionalField = ref('')
const pickup = ref(!Boolean(props.preselectedAddress))
const newCustomer = ref(false)
const selectedCustomerData = ref(null)

function preselectCustomer(customerId) {
    selectedCustomerData.value = customersData.value.find(customer => customer.id === customerId);
}

watch(() => selectedCustomerData.value, () => {
    if (!newCustomer.value) {
        additionalField.value = selectedCustomerData.value?.additional
    }
})

defineExpose({ preselectCustomer })
</script>
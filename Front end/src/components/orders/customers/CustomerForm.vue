<template>
    <!-- <button @click.prevent="(console.log(Boolean(selectedCustomerData)))">#</button> -->
    <div class="row">
        <SelectField divClasses="col-md-6 mb-3" label="Ім'я клієнта" name="name" :directCustomOption="newCustomer"
            :options="filteredCustomersData.map((customer) => customer.name)" customOptionValue="+ Додати нового"
            :preselectedValue="selectedCustomerData ? selectedCustomerData.name : ''"
            @customOptionSelected="() => { newCustomer = true; selectedCustomerData = null }"
            @valueSelected="(option) => selectedCustomerData = customersData.find(customer => customer.name === option)" />
        <SelectField divClasses="col-md-6 mb-3" label="Контакти клієнта" name="contactInfo"
            :directCustomOption="newCustomer" :options="filteredCustomersData.map((customer) => customer.contactInfo)"
            customOptionValue="+ Додати нового"
            :preselectedValue="selectedCustomerData ? selectedCustomerData.contactInfo : ''"
            @customOptionSelected="() => { newCustomer = true; selectedCustomerData = null }"
            @valueSelected="(option) => selectedCustomerData = customersData.find(customer => customer.contactInfo === option)" />
    </div>
    <div class="row" v-if="showAddressInput">
        <SelectField divClasses="col-md-12 mb-3" label="Адреса клієнта" name="address"
            :disabled="!Boolean(selectedCustomerData)" :directCustomOption="newCustomer"
            :options="selectedCustomerData ? selectedCustomerData.addresses : []" customOptionValue="+ Додати нову"
            :preselectedValue="preselectedAddress" />
    </div>
    <div class="row">
        <div class="col-md-12 mb-3">
            <label for="customerAddinional">Додатково</label>
            <input :value="selectedCustomerData ? selectedCustomerData.additional : ''" type="text" class="form-control"
                name="additional" id="customerAddinional" :disabled="!newCustomer">
        </div>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useCustomersStore } from '../../../stores/customers';
import { useSettingsStore } from '@/stores/settings';
import SelectField from '@/components/form_elements/SelectField.vue'
import InputField from '@/components/form_elements/InputField.vue'

const props = defineProps(['showAddressInput', 'preselectedAddress'])

const customersData = computed(() => useCustomersStore().customersData)
const filteredCustomersData = computed(() => customersData.value.filter(customer => !useSettingsStore().settingsData.ordersCustomersToIgnore.includes(customer.contactInfo)))

const newCustomer = ref(false)
const selectedCustomerData = ref(null)

function preselectCustomer(customerId) {
    selectedCustomerData.value = customersData.value.find(customer => customer.id === customerId);
}
defineExpose({ preselectCustomer })
</script>
<template>
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="contactInfo">Контакти клієнта</label>
            <input v-if="newCustomer" type="text" class="form-control" name="contactInfo" id="contactInfo">
            <select v-model="selectedCustomer" v-if="!newCustomer" class="form-select" name="contactInfo"
                id="contactInfo" @change="selectedCustomer === 'new' ? newCustomer = true : {}">
                <option hidden></option>
                <option style="background-color: green;" value="new">+ Додати нового</option>
                <option :value="customer.contactInfo" v-for="customer in customersData">{{ customer.contactInfo }}
                </option>
            </select>
        </div>
        <div class="col-md-6 mb-3">
            <label for="customerName">Ім'я клієнта</label>
            <input :value="selectedCustomerData ? selectedCustomerData.name : ''" type="text" class="form-control"
                name="name" id="customerName" :disabled="!newCustomer">
        </div>
    </div>
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="customerAddress">Адреса клієнта</label>
            <input :value="selectedCustomerData ? selectedCustomerData.address : ''" type="text" class="form-control"
                name="address" id="customerAddress" :disabled="!newCustomer">
        </div>
        <div class="col-md-6 mb-3">
            <label for="customerAddinional">Додатково</label>
            <input :value="selectedCustomerData ? selectedCustomerData.additional : ''" type="text" class="form-control"
                name="additional" id="customerAddinional" :disabled="!newCustomer">
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCustomersStore } from '../../../stores/customers';

const customersData = computed(() => useCustomersStore().customersData)

const newCustomer = ref(false)
const selectedCustomer = ref('')
const selectedCustomerData = computed(() => customersData.value.find(customer => customer.contactInfo === selectedCustomer.value))
</script>
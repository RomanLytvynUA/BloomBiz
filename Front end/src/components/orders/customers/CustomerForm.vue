<template>
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="contactInfo">Контакти клієнта</label>
            <input v-if="newCustomer" type="text" class="form-control" name="customerContacts" id="customerContacts">
            <select v-model="selectedCustomer" v-if="!newCustomer" class="form-select" name="customerContacts"
                id="customerContacts" @change="selectedCustomer === 'new' ? newCustomer = true : {}">
                <option hidden></option>
                <option style="background-color: green;" value="new">+ Додати нового</option>
            </select>
        </div>
        <div class="col-md-6 mb-3">
            <label for="customerName">Ім'я клієнта</label>
            <input type="text" class="form-control" name="name" id="customerName" :disabled="!newCustomer">
        </div>
    </div>
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="customerAddress">Адреса клієнта</label>
            <input type="text" class="form-control" name="address" id="customerAddress" :disabled="!newCustomer">
        </div>
        <div class="col-md-6 mb-3">
            <label for="customerAddinional">Додатково</label>
            <input type="text" class="form-control" name="additional" id="customerAddinional" :disabled="!newCustomer">
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const newCustomer = ref(false)
const selectedCustomer = ref('')
</script>
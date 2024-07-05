<template>
  <h6>НАЛАШТУВАННЯ ВАШОГО МАГАЗИНУ</h6>
  <hr>

  <div class="container">
    <div class="btn-group btn-group-sm d-flex" role="group">
      <button type="button" class="btn btn-success" :disabled="Object.keys(changes).length === 0"
        @click="useSettingsStore().editSettings(changes); changes = {}">Зберегти</button>
      <button type="button" data-bs-toggle="modal" data-bs-target="#resetModal" class="btn btn-danger">Скинути</button>
    </div>
    <!-- <h6>Загальне</h6>
    <div class="row g-2 align-items-center">
      <div class="col-md-5 col-12 mb-3 mb-md-0 me-5" style="margin-top: 0px;">
        <label for="nameInput" class="col-form-label">Назва</label>
        <input type="text" id="nameInput" class="form-control">
      </div>
      <div class="col-md-5 col-12" style="margin-top: 0px;">
        <label for="inputPassword2" class="col-form-label">Пароль</label>
        <div class="input-group">
          <input type="password" class="form-control" value="Password123" readonly>
          <button class="btn btn-primary" type="button">Змінити</button>
        </div>
      </div>
    </div> -->

    <h6>Замовлення</h6>
    <SettingsOption ref="ordersSafetyMode" type="switch" title="Режим безпеки"
      info='Функція "Розібрати Замовлення" не буде доступна поки це налаштування активне.'
      @optionChanged="(value) => changes.ordersSafetyMode = value" />
    <SettingsOption ref="ordersHideOutOfStock" type="switch" title="Приховати товари не в наявності"
      info='Не відображати товари яких немає в наявності при створенні замовлення.'
      @optionChanged="(value) => changes.ordersHideOutOfStock = value" />
    <SettingsAccordion @option-deleted="changes.ordersGoodsToIgnore = ordersGoodsToIgnore;" name="ordersGoodsIngore"
      title="Ігнорувати товари" info="Товари, що не будуть відображенні при створенні замовлення."
      additionModalId="orderGoodsIgnoreModal" :values="ordersGoodsToIgnore" />
    <SettingsAccordion @option-deleted="changes.ordersCustomersToIgnore = ordersCustomersToIgnore;"
      name="ordersCustomersToIgnore" title="Ігнорувати клієнтів"
      info="Клієнти, що не будуть відображенні при створенні замовлення." additionModalId="ordersCustomersIgnoreModal"
      :values="ordersCustomersToIgnore" />
    <SettingsAccordion @option-deleted="changes.ordersStatuses = ordersStatuses;" name="orderStatuses"
      title="Статуси замовлень" additionModalId="addStatusModal"
      info="Статуси, що можуть бути пов'язані з замовленнями." :values="ordersStatuses" />

    <h6>Витрати</h6>
    <SettingsOption ref="expensesSafetyMode" type="switch" title="Режим безпеки"
      info='Функція видалення витрати не буде доступна поки це налаштування активне.'
      @optionChanged="(value) => changes.expensesSafetyMode = value" />
    <SettingsAccordion @option-deleted="changes.expensesSuppliersToIgnore = expensesSuppliersToIgnore;"
      name="expensesSuppliersIngore" title="Ігнорувати постачальників"
      info="Постачальники, що не будуть відображенні при створенні витрати."
      additionModalId="expensesSuppliersIgnoreModal" :values="expensesSuppliersToIgnore" />
    <SettingsAccordion @option-deleted="changes.expensesGoodsToIgnore = expensesGoodsToIgnore;"
      name="expensesGoodsIngore" title="Ігнорувати товари"
      info="Товари, що не будуть відображенні при створенні витрати." additionModalId="expensesGoodsIgnoreModal"
      :values="expensesGoodsToIgnore" />

    <h6>Товари</h6>
    <SettingsOption ref="goodsSafetyMode" type="switch" title="Режим безпеки" info='Функція видалення категорії та товарів не буде доступна поки це налаштування
      активне.' @optionChanged="(value) => changes.goodsSafetyMode = value" />
    <SettingsOption ref="defaultMargin" type="input" title="Націнка за змовченням"
      info='Націнка, що використовується для автоматичного розрахунку ціни товарів.'
      @optionChanged="(value) => changes.defaultMargin = value" />
    <SettingsOption type="btn" title="Скинути ціни"
      info='Всі користувацькі ціни будуть скинуті і автоматично перераховані системою.' modal="#pricesResetModal"
      value="Скинути" />

    <h6>Постачальники</h6>
    <SettingsOption ref="suppliersSafetyMode" type="switch" title="Режим безпеки"
      info='Функція видалення постачальників не буде доступна поки це налаштування активне.'
      @optionChanged="(value) => changes.suppliersSafetyMode = value" />

    <h6>Клієнти</h6>
    <SettingsOption ref="customersSafetyMode" type="switch" title="Режим безпеки"
      info='Функція видалення клієнтів не буде доступна поки це налаштування активне.'
      @optionChanged="(value) => changes.customersSafetyMode = value" />
  </div>

  <StatusAdditionModal
    @statusAdded="(statusName) => { ordersStatuses.push(statusName); changes.ordersStatuses = ordersStatuses; }" />
  <IgnoreModal
    @dataSelected="(productName) => { ordersGoodsToIgnore.push(productName); changes.ordersGoodsToIgnore = ordersGoodsToIgnore; }"
    idPrefix="orderGoods" title="Оберіть товар" labelName="Назва"
    :options="useGoodsStore().goodsNames.filter((product) => !ordersGoodsToIgnore.includes(product))" />
  <IgnoreModal
    @dataSelected="(productName) => { expensesGoodsToIgnore.push(productName); changes.expensesGoodsToIgnore = expensesGoodsToIgnore }"
    idPrefix="expensesGoods" title="Оберіть товар" labelName="Назва"
    :options="useGoodsStore().goodsNames.filter((product) => !expensesGoodsToIgnore.includes(product))" />
  <IgnoreModal
    @dataSelected="(customerName) => { ordersCustomersToIgnore.push(customerName); changes.ordersCustomersToIgnore = ordersCustomersToIgnore }"
    idPrefix="ordersCustomers" title="Оберіть контакти клієнта" labelName="Контакти"
    :options="useCustomersStore().customersContacts.filter((contactInfo) => !ordersCustomersToIgnore.includes(contactInfo))" />
  <IgnoreModal
    @dataSelected="(name) => { expensesSuppliersToIgnore.push(name); changes.expensesSuppliersToIgnore = expensesSuppliersToIgnore }"
    idPrefix="expensesSuppliers" title="Оберіть постачальника" labelName="Ім'я"
    :options="useSuppliersStore().suppliersNames.filter((name) => !expensesSuppliersToIgnore.includes(name))" />
  <ResetModal @reset="useSettingsStore().resetSettings(); changes = {};" />
  <PricesResetModal />
</template>
<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useGoodsStore } from '../../stores/goods';
import { useCustomersStore } from '../../stores/customers';
import { useSuppliersStore } from '../../stores/suppliers';
import { useSettingsStore } from '../../stores/settings';

import SettingsOption from './settingsComponents/SettingsOption.vue';
import SettingsAccordion from './settingsComponents/SettingsAccordion.vue';

import StatusAdditionModal from './settingsComponents/StatusAdditionModal.vue';
import IgnoreModal from './settingsComponents/IgnoreModal.vue';
import PricesResetModal from './settingsComponents/PricesResetModal.vue';
import ResetModal from './settingsComponents/ResetModal.vue';


const changes = ref({})
const settingsData = computed(() => useSettingsStore().settingsData)

const ordersSafetyMode = ref(null)
const ordersHideOutOfStock = ref(null)
const ordersGoodsToIgnore = ref([]);
const ordersCustomersToIgnore = ref([]);
const ordersStatuses = ref(settingsData.ordersStatuses);

const expensesSafetyMode = ref(null);
const expensesGoodsToIgnore = ref([]);
const expensesSuppliersToIgnore = ref([]);

const goodsSafetyMode = ref(null);
const defaultMargin = ref(null);

const suppliersSafetyMode = ref(null);

const customersSafetyMode = ref(null);

// Only keep actual changes
watch(() => changes.value, (data) => {
  Object.keys(data).forEach(key => {
    if (String(data[key]) === String(settingsData.value[key])) {
      delete changes.value[key]
    }
  });
}, { deep: true })

// Repopulate settings when data changed
watch(() => settingsData.value, (data) => {
  populateSettings(data)
}, { deep: true });

// Populate settings when first opened
onMounted(() => populateSettings(settingsData.value))

function populateSettings(data) {
  ordersSafetyMode.value.switchInput = data.ordersSafetyMode;
  ordersHideOutOfStock.value.switchInput = data.ordersHideOutOfStock;
  ordersGoodsToIgnore.value = [...data.ordersGoodsToIgnore];
  ordersCustomersToIgnore.value = [...data.ordersCustomersToIgnore];
  ordersStatuses.value = [...data.ordersStatuses];

  expensesSafetyMode.value.switchInput = data.expensesSafetyMode;
  expensesGoodsToIgnore.value = [...data.expensesGoodsToIgnore];
  expensesSuppliersToIgnore.value = [...data.expensesSuppliersToIgnore];

  goodsSafetyMode.value.switchInput = data.goodsSafetyMode;
  defaultMargin.value.intInput = data.defaultMargin;

  suppliersSafetyMode.value.switchInput = data.suppliersSafetyMode;

  customersSafetyMode.value.switchInput = data.customersSafetyMode;
}
</script>

<style scoped>
h6 {
  margin-top: 6px;
}
</style>

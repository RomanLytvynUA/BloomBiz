<template>
  <h6>{{ t('dashboard.settings.title') }}</h6>
  <hr>

  <div class="container">
    <div class="btn-group btn-group-sm d-flex" role="group">
      <button type="button" class="btn btn-success" :disabled="Object.keys(changes).length === 0"
        @click="useSettingsStore().editSettings(changes); changes = {}">{{ t('general.saveBtnText')
        }}</button>
      <button type="button" data-bs-toggle="modal" data-bs-target="#resetModal" class="btn btn-danger">{{
    t('general.resetBtnText') }}</button>
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

    <h6>{{ t('dashboard.settings.orders.title') }}</h6>
    <SettingsOption ref="ordersSafetyMode" type="switch" :title="t('dashboard.settings.orders.safetyModeTitle')"
      :info="t('dashboard.settings.orders.safetyModeDescription')"
      @optionChanged="(value) => changes.ordersSafetyMode = value" />
    <SettingsOption ref="ordersHideOutOfStock" type="switch" :title="t('dashboard.settings.orders.hideOutOfStockTitle')"
      :info="t('dashboard.settings.orders.hideOutOfStockDescription')"
      @optionChanged="(value) => changes.ordersHideOutOfStock = value" />
    <SettingsAccordion @option-deleted="changes.ordersGoodsToIgnore = ordersGoodsToIgnore;" name="ordersGoodsIngore"
      :title="t('dashboard.settings.orders.ignoreGoodsTitle')"
      :info="t('dashboard.settings.orders.ignoreGoodsDescription')" additionModalId="orderGoodsIgnoreModal"
      :values="ordersGoodsToIgnore" />
    <SettingsAccordion @option-deleted="changes.ordersCustomersToIgnore = ordersCustomersToIgnore;"
      name="ordersCustomersToIgnore" :title="t('dashboard.settings.orders.ignoreCustomersTitle')"
      :info="t('dashboard.settings.orders.ignoreCustomersDescription')" additionModalId="ordersCustomersIgnoreModal"
      :values="ordersCustomersToIgnore" />
    <SettingsAccordion @option-deleted="changes.ordersStatuses = ordersStatuses;" name="orderStatuses"
      :title="t('dashboard.settings.orders.statusesTitle')" additionModalId="addStatusModal"
      :info="t('dashboard.settings.orders.statusesDescription')" :values="ordersStatuses" />

    <h6>{{ t('dashboard.settings.expenses.title') }}</h6>
    <SettingsOption ref="expensesSafetyMode" type="switch" :title="t('dashboard.settings.expenses.safetyModeTitle')"
      :info="t('dashboard.settings.expenses.safetyModeDescription')"
      @optionChanged="(value) => changes.expensesSafetyMode = value" />
    <SettingsAccordion @option-deleted="changes.expensesSuppliersToIgnore = expensesSuppliersToIgnore;"
      name="expensesSuppliersIngore" :title="t('dashboard.settings.expenses.ignoreSuppliersTitle')"
      :info="t('dashboard.settings.expenses.ignoreSuppliersDescription')" additionModalId="expensesSuppliersIgnoreModal"
      :values="expensesSuppliersToIgnore" />
    <SettingsAccordion @option-deleted="changes.expensesGoodsToIgnore = expensesGoodsToIgnore;"
      name="expensesGoodsIngore" :title="t('dashboard.settings.expenses.ignoreGoodsTitle')"
      :info="t('dashboard.settings.expenses.ignoreGoodsDescription')" additionModalId="expensesGoodsIgnoreModal"
      :values="expensesGoodsToIgnore" />

    <h6>{{ t('dashboard.settings.goods.title') }}</h6>
    <SettingsOption ref="goodsSafetyMode" type="switch" :title="t('dashboard.settings.goods.safetyModeTitle')"
      :info="t('dashboard.settings.goods.safetyModeDescription')"
      @optionChanged="(value) => changes.goodsSafetyMode = value" />
    <SettingsOption ref="defaultMargin" type="input" :title="t('dashboard.settings.goods.defaultMarginTitle')"
      :info="t('dashboard.settings.goods.defaultMarginDescription')"
      @optionChanged="(value) => changes.defaultMargin = value" />
    <SettingsOption type="resetBtn" :title="t('dashboard.settings.goods.resetPricesTitle')"
      :info="t('dashboard.settings.goods.resetPricesDescription')" modal="#pricesResetModal" />

    <h6>{{ t('dashboard.settings.suppliers.title') }}</h6>
    <SettingsOption ref="suppliersSafetyMode" type="switch" :title="t('dashboard.settings.suppliers.safetyModeTitle')"
      :info="t('dashboard.settings.suppliers.safetyModeDescription')"
      @optionChanged="(value) => changes.suppliersSafetyMode = value" />

    <h6>{{ t('dashboard.settings.customers.title') }}</h6>
    <SettingsOption ref="customersSafetyMode" style="margin-bottom: 0 !important;" type="switch"
      :title="t('dashboard.settings.customers.safetyModeTitle')"
      :info="t('dashboard.settings.customers.safetyModeDescription')"
      @optionChanged="(value) => changes.customersSafetyMode = value" />
  </div>

  <StatusAdditionModal
    @statusAdded="(statusName) => { ordersStatuses.push(statusName); changes.ordersStatuses = ordersStatuses; }" />
  <IgnoreModal
    @dataSelected="(productName) => { ordersGoodsToIgnore.push(productName); changes.ordersGoodsToIgnore = ordersGoodsToIgnore; }"
    idPrefix="orderGoods" :title="t('dashboard.settings.orders.goodsToIgnoreModalTitle')"
    :labelName="t('dashboard.settings.orders.goodsToIgnoreModalLabelName')"
    :options="useGoodsStore().goodsNames.filter((product) => !ordersGoodsToIgnore.includes(product))" />
  <IgnoreModal
    @dataSelected="(productName) => { expensesGoodsToIgnore.push(productName); changes.expensesGoodsToIgnore = expensesGoodsToIgnore }"
    idPrefix="expensesGoods" :title="t('dashboard.settings.expenses.goodsToIgnoreModalTitle')"
    :labelName="t('dashboard.settings.expenses.goodsToIgnoreModalLabelName')"
    :options="useGoodsStore().goodsNames.filter((product) => !expensesGoodsToIgnore.includes(product))" />
  <IgnoreModal
    @dataSelected="(customerName) => { ordersCustomersToIgnore.push(customerName); changes.ordersCustomersToIgnore = ordersCustomersToIgnore }"
    idPrefix="ordersCustomers" :title="t('dashboard.settings.orders.customersToIgnoreModalTitle')"
    :labelName="t('dashboard.settings.orders.customersToIgnoreModalLabelName')"
    :options="useCustomersStore().customersContacts.filter((contactInfo) => !ordersCustomersToIgnore.includes(contactInfo))" />
  <IgnoreModal
    @dataSelected="(name) => { expensesSuppliersToIgnore.push(name); changes.expensesSuppliersToIgnore = expensesSuppliersToIgnore }"
    idPrefix="expensesSuppliers" :title="t('dashboard.settings.expenses.suppliersToIgnoreModalTitle')"
    :labelName="t('dashboard.settings.expenses.suppliersToIgnoreModalLabelName')"
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

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

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

// Populate settings when tha page first opened
onMounted(() => populateSettings(settingsData.value))

function populateSettings(data) {
  ordersSafetyMode.value.switchInput = data.ordersSafetyMode || false;
  ordersHideOutOfStock.value.switchInput = data.ordersHideOutOfStock || false;
  ordersGoodsToIgnore.value = [...(data.ordersGoodsToIgnore || [])];
  ordersCustomersToIgnore.value = [...(data.ordersCustomersToIgnore || [])];
  ordersStatuses.value = [...(data.ordersStatuses || [])];

  expensesSafetyMode.value.switchInput = data.expensesSafetyMode || false;
  expensesGoodsToIgnore.value = [...(data.expensesGoodsToIgnore || [])];
  expensesSuppliersToIgnore.value = [...(data.expensesSuppliersToIgnore || [])];

  goodsSafetyMode.value.switchInput = data.goodsSafetyMode || false;
  defaultMargin.value.intInput = data.defaultMargin || 0;

  suppliersSafetyMode.value.switchInput = data.suppliersSafetyMode || false;

  customersSafetyMode.value.switchInput = data.customersSafetyMode || false;
}
</script>

<style scoped>
h6 {
  margin-top: 6px;
}
</style>

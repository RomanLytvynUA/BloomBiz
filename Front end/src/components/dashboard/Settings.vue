<template>
  <h6>НАЛАШТУВАННЯ ВАШОГО МАГАЗИНУ</h6>
  <hr>

  <div class="container">
    <div class="btn-group btn-group-sm d-flex" role="group">
      <button type="button" class="btn btn-success" :disabled="Object.keys(changes).length === 0"
        @click="console.log(changes)">Зберегти</button>
      <button type="button" data-bs-toggle="modal" data-bs-target="#resetModal" class="btn btn-danger">Скинути</button>
    </div>
    <h6>Загальне</h6>
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
    </div>

    <h6>Замовлення</h6>
    <SettingsOption ref="orderSafetyMode" type="switch" title="Режим безпеки"
      info='Функція "Розібрати Замовлення" не буде доступна поки це налаштування активне.'
      @optionChanged="(value) => changes.orderSafetyMode = value" />
    <SettingsOption ref="orderHideOutOfStock" type="switch" title="Приховати товари не в наявності"
      info='Не відображати товари яких немає в наявності при створенні замовлення.'
      @optionChanged="(value) => changes.orderHideOutOfStock = value" />
    <SettingsAccordion @option-deleted="changes.orderGoodsToIgnore = orderGoodsToIgnore;" name="orderGoodsIngore"
      title="Ігнорувати товари" info="*товари, що не будуть відображенні при створенні замовлення."
      additionModalId="orderGoodsIgnoreModal" :values="orderGoodsToIgnore" />
    <SettingsAccordion @option-deleted="changes.orderStatuses = orderStatuses;" name="orderStatuses"
      title="Статуси замовлень" additionModalId="addStatusModal"
      info="*статуси, що можуть бути пов'язані з замовленнями." :values="orderStatuses" />

    <h6>Витрати</h6>
    <SettingsOption ref="expensesSafetyMode" type="switch" title="Режим безпеки"
      info='Функція видалення витрати не буде доступна поки це налаштування активне.'
      @optionChanged="(value) => changes.expensesSafetyMode = value" />
    <SettingsAccordion @option-deleted="changes.expensesSuppliersToIgnore = expensesSuppliersToIgnore;"
      name="expensesSuppliersIngore" title="Ігнорувати постачальників"
      info="*постачальники, що не будуть відображенні при створенні витрати."
      additionModalId="expensesSuppliersIgnoreModal" :values="expensesSuppliersToIgnore" />
    <SettingsAccordion @option-deleted="changes.expensesGoodsToIgnore = expensesGoodsToIgnore;"
      name="expensesGoodsIngore" title="Ігнорувати товари"
      info="*товари, що не будуть відображенні при створенні витрати." additionModalId="expensesGoodsIgnoreModal"
      :values="expensesGoodsToIgnore" />

    <h6>Товари</h6>
    <SettingsOption ref="goodsSafetyMode" type="switch" title="Режим безпеки" info='Функція видалення категорії та товарів не буде доступна поки це налаштування
      активне.' @optionChanged="(value) => changes.goodsSafetyMode = value" />
    <SettingsOption ref="goodsMargin" type="input" title="Націнка за змовченням"
      info='Націнка, що використовується для автоматичного розрахунку ціни товарів.' value="125"
      @optionChanged="(value) => changes.goodsMargin = value" />
    <SettingsOption type="btn" title="Скинути ціни"
      info='Всі користувацькі ціни будуть скинуті і автоматично перераховані системою.' modal="#pricesResetModal"
      value="Скинути" />

    <h6>Постачальники</h6>
    <SettingsOption ref="suppliersSafetyMode" type="switch" title="Режим безпеки"
      info='Функція видалення постачальників не буде доступна поки це налаштування активне.'
      @optionChanged="(value) => changes.suppliersSafetyMode = value" />
  </div>

  <StatusAdditionModal
    @statusAdded="(statusName) => { orderStatuses.push(statusName); changes.orderStatuses = orderStatuses; }" />
  <IgnoreModal
    @dataSelected="(productName) => { orderGoodsToIgnore.push(productName); changes.orderGoodsToIgnore = orderGoodsToIgnore; }"
    idPrefix="orderGoods" title="Оберіть товар" labelName="Назва"
    :options="useGoodsStore().goodsNames.filter((product) => !orderGoodsToIgnore.includes(product))" />
  <IgnoreModal
    @dataSelected="(productName) => { expensesGoodsToIgnore.push(productName); changes.expensesGoodsToIgnore = expensesGoodsToIgnore }"
    idPrefix="expensesGoods" title="Оберіть товар" labelName="Назва"
    :options="useGoodsStore().goodsNames.filter((product) => !expensesGoodsToIgnore.includes(product))" />
  <IgnoreModal
    @dataSelected="(name) => { expensesSuppliersToIgnore.push(name); changes.expensesSuppliersToIgnore = expensesSuppliersToIgnore }"
    idPrefix="expensesSuppliers" title="Оберіть постачальника" labelName="Ім'я"
    :options="useSuppliersStore().suppliersNames.filter((name) => !expensesSuppliersToIgnore.includes(name))" />
  <PricesResetModal />
  <ResetModal />
</template>
<script setup>
import { ref, watch } from 'vue';
import { useGoodsStore } from '../../stores/goods';
import { useSuppliersStore } from '../../stores/suppliers';

import SettingsOption from './settingsComponents/SettingsOption.vue';
import SettingsAccordion from './settingsComponents/SettingsAccordion.vue';

import StatusAdditionModal from './settingsComponents/StatusAdditionModal.vue';
import IgnoreModal from './settingsComponents/IgnoreModal.vue';
import PricesResetModal from './settingsComponents/PricesResetModal.vue';
import ResetModal from './settingsComponents/ResetModal.vue';

const changes = ref({})

const orderSafetyMode = ref(null)
const orderHideOutOfStock = ref(null)
const orderGoodsToIgnore = ref([]);
const orderStatuses = ref(["Продано", "Списано", "Вітрина"]);

const expensesSafetyMode = ref(null);
const expensesGoodsToIgnore = ref([]);
const expensesSuppliersToIgnore = ref([]);

const goodsSafetyMode = ref(null);
const goodsMargin = ref(null);

const suppliersSafetyMode = ref(null);
</script>

<style scoped>
h6 {
  margin-top: 6px;
}
</style>

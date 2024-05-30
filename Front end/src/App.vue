<script setup>
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useSuppliersStore } from '@/stores/suppliers'
import { useExpensesStore } from '@/stores/expenses'
import { useGoodsStore } from '@/stores/goods'
import { useOrdersStore } from '@/stores/orders'
import { useSettingsStore } from '@/stores/settings'


// Call when the component is added to the html div
onMounted(() => {
  useSuppliersStore().fetchSuppliers();
  useExpensesStore().fetchExpenses();
  useGoodsStore().fetchGoods();
  useOrdersStore().fetchOrders();
  useSettingsStore().fetchSettings();
});
</script>

<template>
  <Navbar />
  <RouterView />
</template>

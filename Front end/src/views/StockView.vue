<template>
  <Headline title="Товари на складі"
    description="Тут ви можете переглянути товари, які у вас є та списати їх. Нові позиції будуть додані на склад одразу після реєстрації нової витрати." />

  <TableComponent ref="tableComponent" :loading="loading" @filterChanged="filterGoods" :filters="tableFilters"
    :headers="tableHeaders" :rows="tableRows" />
</template>

<script setup>
import { ref, computed, markRaw, watch, onMounted } from 'vue'
import { useGoodsStore } from '../stores/goods';

import Headline from '../components/Headline.vue'

import TableComponent from '../components/table_elements/TableComponent.vue';
import DecommissionBtnGroup from '../components/table_elements/DecommissionBtnGroup.vue';
import PriceControl from '../components/table_elements/PriceControl.vue';
import SelectFilter from '../components/table_elements/filters/SelectFilter.vue';
import InputFilter from '../components/table_elements/filters/InputFilter.vue';

// get and filter data
const loading = computed(() => useGoodsStore().inLoadingState);
const goodsData = computed(() => useGoodsStore().inStockGoodsData)
const categoriesData = computed(() => useGoodsStore().categoriesNames)
const filteredGoods = ref([])

async function filterGoods() {
  if (tableComponent.value) {
    const categoryFilterComponent = tableComponent.value.$refs.categoryFilterComponent[0];
    const productFilterComponent = tableComponent.value.$refs.productFilterComponent[0];
    const quantityFilterComponent = tableComponent.value.$refs.quantityFilterComponent[0];

    filteredGoods.value = goodsData.value.filter(product => {
      return (
        categoryFilterComponent.filterData(product.category) &&
        productFilterComponent.filterData(product.product) &&
        (() => {
          const quantityFilter = quantityFilterComponent.getChoice();
          switch (quantityFilter) {
            case "В наявності":
              return Number(product.quantity) > 0;
            case "Не в наявності":
              return Number(product.quantity) === 0;
            case "Погрішність":
              return Number(product.quantity) < 0;
            case "В асортименті":
              return true;
            default:
              return false;
          }
        })()
      );
    });
  }
}

watch(goodsData, filterGoods)

// table staff
const tableComponent = ref(null);

const tableFilters = ref([
  { component: markRaw(SelectFilter), reference: 'categoryFilterComponent', props: { options: categoriesData } },
  { component: markRaw(InputFilter), reference: 'productFilterComponent', props: { placeholder: 'Введіть назву товару...' } },
  { component: markRaw(SelectFilter), reference: 'quantityFilterComponent', props: { options: ["В асортименті", "Не в наявності", "Погрішність"], defaultText: "В наявності" } },
])

const tableHeaders = ref([
  { 'name': 'Категорія', 'size': '25%' },
  { 'name': 'Товар', 'size': '30%' },
  { 'name': 'Кількість', 'size': '15%' },
  { 'name': 'Ціна', 'size': '12%' },
  { 'name': 'Дія', 'size': '18%' },
]);

const tableRows = computed(() => filteredGoods.value.map(product => [
  product.category,
  product.product,
  `${product.quantity} ${product.units}`,
  {
    component: PriceControl,
    props: {
      prefilledValue: product.price,
      productId: product.id,
    },
  },
  {
    component: DecommissionBtnGroup,
    props: {
      productName: product.product,
      productCategory: product.category,
    },
  },
]));

onMounted(() => {
  filterGoods()

})
</script>
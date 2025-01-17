<template>
  <Headline :title="t('stock.title')" :description="t('stock.description')" />

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

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

// get and filter data
const loading = computed(() => useGoodsStore().inLoadingState);
const goodsData = computed(() => useGoodsStore().goodsData);
const categoriesData = computed(() => useGoodsStore().categoriesNames);
const filteredGoods = ref([]);

async function filterGoods() {
  filteredGoods.value = [];
  if (tableComponent.value) {
    const categoryFilterComponent = tableComponent.value.$refs.categoryFilterComponent[0];
    const productFilterComponent = tableComponent.value.$refs.productFilterComponent[0];
    const quantityFilterComponent = tableComponent.value.$refs.quantityFilterComponent[0];

    for (const category of goodsData.value) {
      if (!categoryFilterComponent.filterData(category.name)) {
        continue;
      }

      filteredGoods.value = filteredGoods.value.concat(...category.goods.filter(product => {
        product.categoryName = category.name
        product.categoryUnits = category.units
        const passesNameFilter = productFilterComponent.filterData(product.name);

        const quantityFilter = quantityFilterComponent.getChoice();
        const passesQuantityFilter = (() => {
          switch (quantityFilter) {
            case t('stock.filters.quantity.in-stock'):
              return Number(product.quantity) > 0;
            case t('stock.filters.quantity.out-of-stock'):
              return Number(product.quantity) === 0;
            case t('stock.filters.quantity.invalid'):
              return Number(product.quantity) < 0;
            case t('stock.filters.quantity.in-assortment'):
              return true;
            default:
              return false;
          }
        })();

        return passesNameFilter && passesQuantityFilter;
      }));
    }
  }
}

watch(goodsData, filterGoods)

// table staff
const tableComponent = ref(null);

const tableFilters = ref([
  { component: markRaw(SelectFilter), reference: 'categoryFilterComponent', props: { options: categoriesData } },
  { component: markRaw(InputFilter), reference: 'productFilterComponent', props: { placeholder: computed(() => t('stock.filters.enterProduct')) } },
  {
    component: markRaw(SelectFilter), reference: 'quantityFilterComponent',
    props: {
      options: computed(() => [t('stock.filters.quantity.in-assortment'),
      t('stock.filters.quantity.out-of-stock'), t('stock.filters.quantity.invalid')]), defaultText: computed(() => t('stock.filters.quantity.in-stock'))
    }
  },
])

const tableHeaders = ref([
  { 'name': computed(() => t('stock.tableHeaders.category')), 'size': '25%' },
  { 'name': computed(() => t('stock.tableHeaders.product')), 'size': '30%' },
  { 'name': computed(() => t('stock.tableHeaders.quantity')), 'size': '15%' },
  { 'name': computed(() => t('stock.tableHeaders.price')), 'size': '10%' },
  { 'name': computed(() => t('stock.tableHeaders.action')), 'size': '20%' },
]);

const tableRows = computed(() => filteredGoods.value.map(product => [
  product.categoryName,
  product.name,
  `${product.quantity} ${product.categoryUnits}`,
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
      productId: product.id
    },
  },
]));

onMounted(() => {
  filterGoods()

})
</script>
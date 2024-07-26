<template>
  <h6>{{ t("dashboard.statistics.title") }}</h6>
  <hr>
  <IncomeChart />
</template>

<script setup>
import IncomeChart from './statisticsComponents/IncomeChart.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>

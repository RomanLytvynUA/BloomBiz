<template>
  <Headline :title="t('dashboard.title')" description="" />
  <br>
  <div class="container">
    <div class="row gutters-sm">
      <div class="col-md-3 d-none d-lg-block">
        <div class="card">
          <div class="card-body">
            <nav class="nav flex-column nav-pills nav-gap-y-1">
              <a href="#statistic" class="nav-item nav-link has-icon nav-link-faded"
                :class="{ 'active': isActiveLink('statistic') }">
                <svg class="bi me-2" width="24" height="24" fill="currentColor">
                  <use :xlink:href="`${icons}#icon-chart`"></use>
                </svg>
                {{ t("dashboard.statistics.name") }}
              </a>
              <a href="#assortment" class="nav-item nav-link has-icon nav-link-faded"
                :class="{ 'active': isActiveLink('assortment') }">
                <svg class="bi me-2" width="24" height="24" fill="currentColor">
                  <use :xlink:href="`${icons}#icon-shop`"></use>
                </svg>
                {{ t("dashboard.assortment.name") }}
              </a>
              <!-- <a href="#calendar" class="nav-item nav-link has-icon nav-link-faded active"
                  :class="{ 'active': isActiveLink('calendar') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-calendar`"></use>
                  </svg>
                  Календар
                </a> -->
              <a href="#settings" class="nav-item nav-link has-icon nav-link-faded"
                :class="{ 'active': isActiveLink('settings') }">
                <svg class="bi me-2" width="24" height="24" fill="currentColor">
                  <use :xlink:href="`${icons}#icon-gear`"></use>
                </svg>
                {{ t("dashboard.settings.name") }}
              </a>
            </nav>
          </div>
        </div>
      </div>
      <div class="col-lg-9">
        <div class="card">
          <div class="card-header border-bottom mb-3 d-flex d-lg-none">
            <ul class="nav nav-tabs card-header-tabs nav-gap-x-1" role="tablist">
              <li class="nav-item">
                <a href="#statistic" data-toggle="tab" class="nav-link has-icon"
                  :class="{ 'active': isActiveLink('statistic') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-chart`"></use>
                  </svg>
                </a>
              </li>
              <li class="nav-item">
                <a href="#assortment" data-toggle="tab" class="nav-link has-icon"
                  :class="{ 'active': isActiveLink('assortment') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-shop`"></use>
                  </svg>
                </a>
              </li>
              <li>
                <!-- <a href="#calendar" data-toggle="tab" class="nav-link has-icon"
                    :class="{ 'active': isActiveLink('calendar') }">
                    <svg class="bi me-2" width="24" height="24" fill="currentColor">
                      <use :xlink:href="`${icons}#icon-calendar`"></use>
                    </svg>
                  </a> -->
              </li>
              <li>
                <a href="#settings" data-toggle="tab" class="nav-link has-icon"
                  :class="{ 'active': isActiveLink('settings') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-gear`"></use>
                  </svg>
                </a>
              </li>
            </ul>
          </div>
          <div class="card-body tab-content">
            <Statistics v-if="isActiveLink('statistic')" />
            <Assortment v-if="isActiveLink('assortment')" />
            <Settings v-if="isActiveLink('settings')" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <br>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import icons from '@/assets/icons.svg'

import Headline from '../components/Headline.vue'

import Statistics from '../components/dashboard/Statistics.vue'
import Assortment from '../components/dashboard/Assortment.vue'
import Settings from '../components/dashboard/Settings.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const router = useRouter();

const isActiveLink = (linkId) => {
  if (router.currentRoute.value.hash === "") { router.currentRoute.value.hash = "#statistic" }
  let isActive = false;
  watchEffect(() => {
    isActive = router.currentRoute.value.hash === `#${linkId}`;
  });
  return isActive;
};
</script>

<style scoped>
.nav-link {
  color: #4a5568;
}

.nav-item {
  color: gray;
  font-weight: 500;
}

.nav-item.active {
  background-color: #f8f9fa;
  color: black;
}

.card {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .1), 0 1px 2px 0 rgba(0, 0, 0, .06);
}

.me-2 {
  margin: 0px !important;
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 0 solid rgba(0, 0, 0, .125);
  border-radius: .25rem;
}

.card-body {
  flex: 1 1 auto;
  min-height: 1px;
  padding: 1rem;
}

.gutters-sm {
  margin-right: -8px;
  margin-left: -8px;
}

.gutters-sm>.col,
.gutters-sm>[class*=col-] {
  padding-right: 8px;
  padding-left: 8px;
}

.mb-3,
.my-3 {
  margin-bottom: 1rem !important;
}

.bg-gray-300 {
  background-color: #e2e8f0;
}
</style>
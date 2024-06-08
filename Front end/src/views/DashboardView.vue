<template>
  <div>
    <Headline title="Кабінет" description="" />
    <br>
    <div class="container">
      <div class="row">
        <div class="col-12 col-md-3 order-0 order-md-0">
          <div class="card mb-3">
            <div class="card-body">
              <nav class="nav flex-column nav-pills nav-gap-y-1" style="max-width: 250px; overflow-y: auto;">
                <a href="#statistic" class="nav-item nav-link has-icon nav-link-faded d-flex align-items-center"
                  :class="{ 'active': isActiveLink('statistic') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-chart`"></use>
                  </svg>
                  Статистика
                </a>
                <a href="#assortment" class="nav-item nav-link has-icon nav-link-faded d-flex align-items-center"
                  :class="{ 'active': isActiveLink('assortment') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-shop`"></use>
                  </svg>
                  Асортимент
                </a>
                <!-- <a href="#calendar" class="nav-item nav-link has-icon nav-link-faded d-flex align-items-center"
                  :class="{ 'active': isActiveLink('calendar') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-calendar`"></use>
                  </svg>
                  Календар
                </a> -->
                <a href="#settings" class="nav-item nav-link has-icon nav-link-faded d-flex align-items-center"
                  :class="{ 'active': isActiveLink('settings') }">
                  <svg class="bi me-2" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-gear`"></use>
                  </svg>
                  Налаштування
                </a>
              </nav>
            </div>
          </div>
        </div>

        <!-- Main content: occupies full width on small screens and 75% on medium and larger screens -->
        <div class="col-12 col-md-9 order-1 order-md-1">
          <div class="card">
            <div class="card-body">
              <Statistics v-if="isActiveLink('statistic')" />
              <Assortment v-if="isActiveLink('assortment')" />
              <Settings v-if="isActiveLink('settings')" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import icons from '@/icons.svg'

import Headline from '../components/Headline.vue'

import Statistics from '../components/dashboard/Statistics.vue'
import Assortment from '../components/dashboard/Assortment.vue'
import Settings from '../components/dashboard/Settings.vue'

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
.nav-item {
  /* color: black; */
  color: gray;
  font-weight: 500;
}

.nav-item.active {
  /* background-color: #206d4b; */
  background-color: #f8f9fa;
  color: black;
}
</style>
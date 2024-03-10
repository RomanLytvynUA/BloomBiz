<template>
  <div>
    <Headline title="Кабінет" description="" />
    <br>
    <div class="container">
      <div class="row">
        <div class="col-md-3 d-none d-md-block">
          <div class="card">
            <div class="card-body">
              <nav class="nav flex-column nav-pills nav-gap-y-1">
                <a href="#statistic" class="nav-item nav-link has-icon nav-link-faded" :class="{ 'active': isActiveLink('statistic') }">
                  <svg class="bi" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-chart`"></use>
                  </svg>
                    Статистика
                </a>
                <a href="#assortment" class="nav-item nav-link has-icon nav-link-faded" :class="{ 'active': isActiveLink('assortment') }">
                  <svg class="bi" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-shop`"></use>
                  </svg>
                    Асортимент
                </a>
                <a href="#crm" class="nav-item nav-link has-icon nav-link-faded" :class="{ 'active': isActiveLink('crm') }">
                  <svg class="bi" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-person`"></use>
                  </svg>
                    Клієнти
                </a>
                <a href="#calendar" class="nav-item nav-link has-icon nav-link-faded" :class="{ 'active': isActiveLink('calendar') }">
                  <svg class="bi" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-calendar`"></use>
                  </svg>
                    Календар
                </a>
                <a href="#settings" class="nav-item nav-link has-icon nav-link-faded" :class="{ 'active': isActiveLink('settings') }">
                  <svg class="bi" width="24" height="24" fill="currentColor">
                    <use :xlink:href="`${icons}#icon-gear`"></use>
                  </svg>
                    Налаштування
                </a>
              </nav>
            </div>
          </div>
        </div>
        <div class="col-md-9">
          <div class="card">
            <div class="card-body">
              <div>
                <h6>ВАША СТАТИСТИКА</h6>
                <hr>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import icons from '@/icons.svg'

import Headline from '../components/Headline.vue'

const router = useRouter();

const isActiveLink = (linkId) => {
  if (router.currentRoute.value.hash === "") {router.currentRoute.value.hash = "#statistic"}
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
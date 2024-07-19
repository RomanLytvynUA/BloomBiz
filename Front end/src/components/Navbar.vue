<template>
  <nav class="navbar navbar-expand-lg sticky-top bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">
        <img src="../assets/logo.png" alt="Логотип" width="30" height="30" class="d-inline-block align-text-top">
        BloomBiz
      </RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-if="useAuthStore().isAuthenticated" v-for="route in routes" :key="route.name" class="nav-item">
            <RouterLink :class="['nav-link', { 'active': $route.name === route.name }]" :to="route.path">
              {{ t(`navbar.${route.name}`) }}
            </RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item dropdown" style="padding-right: 16px;">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              {{ t('localeShortName') }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <button v-for="availableLocale in availableLocales" class="dropdown-item"
                @click.prevent="setLocale(availableLocale)">
                {{ getLocaleMessage(availableLocale).localeName }}
              </button>
            </ul>
          </li>
          <li class="nav-item d-flex align-items-center" v-if="useAuthStore().isAuthenticated">
            <svg xmlns="http://www.w3.org/2000/svg" id="icon-logout" width="16" height="16" fill="currentColor"
              class="bi bi-box-arrow-right" viewBox="0 0 16 16">
              <path fill-rule="evenodd"
                d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z" />
              <path fill-rule="evenodd"
                d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z" />
            </svg>
            <a class="nav-link" style="padding-left: 5px;" @click="useAuthStore().logout()">
              {{ t('navbar.signout') }}
            </a>
          </li>
          <li class="nav-item d-flex align-items-center" v-if="!useAuthStore().isAuthenticated">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
              class="bi bi-box-arrow-in-right" viewBox="0 0 16 16">
              <path fill-rule="evenodd"
                d="M6 3.5a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-2a.5.5 0 0 0-1 0v2A1.5 1.5 0 0 0 6.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-8A1.5 1.5 0 0 0 5 3.5v2a.5.5 0 0 0 1 0z" />
              <path fill-rule="evenodd"
                d="M11.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H1.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z" />
            </svg>
            <RouterLink style="padding-left: 5px;" :class="['nav-link', { 'active': $route.name === 'signin' }]"
              to="/signin">{{ t(`navbar.signin`) }}
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useI18n } from 'vue-i18n';
const { t, locale, availableLocales, getLocaleMessage } = useI18n({ useScope: 'global' })

const router = useRouter();
const routes = router.options.routes.filter(route => !['home', 'signin'].includes(route.name));

const setLocale = (localeName) => {
  locale.value = localeName;
  localStorage.setItem('lang', localeName);
}
</script>

<style scoped>
.nav-item:hover {
  cursor: pointer;
}

.dropdown-item:focus {
  background-color: #ebeef0 !important;
  color: #fff !important;
}

.dropdown-menu {
  padding: 1px !important;
  margin: 0 !important;
  min-width: auto !important;
}
</style>
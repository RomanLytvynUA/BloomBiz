<template>
  <nav class="navbar navbar-expand-lg sticky-top bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">
        <img src="../assets/logo.png" alt="Логотип" width="30" height="30" class="d-inline-block align-text-top">
        BloomBiz
      </RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-for="route in routes" :key="route.name" class="nav-item">
            <RouterLink :class="['nav-link', { 'active': $route.name === route.name }]" :to="route.path">{{ route.name }}</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
  import { useRouter, RouterLink } from 'vue-router';
  const router = useRouter();
  const routes = router.options.routes.filter(route => route.name !== 'home');
</script>
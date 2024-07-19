<template>
    <br>
    <div class="container-fluid text-center py-5" style="padding-top: 0 !important;">
        <div id="logo">
            <img src="../assets/logo.png" width="190" class="img-fluid mx-auto d-block" alt="логотип">
            <figure style="margin-bottom: 0px;">
                <blockquote class="blockquote">
                    <h1>{{ t('home.welcome') }}</h1>
                </blockquote>
                <figcaption class="blockquote-footer" style="margin-bottom: 0px;">
                    {{ t('home.tagline') }}
                </figcaption>
            </figure>
        </div>
    </div>

    <div v-if="!useAuthStore().isAuthenticated" class="text-center d-flex justify-content-center">
        <RouterLink to="/signin">
            <button class="btn btn-success btn-lg">{{ t('home.start') }}</button>
        </RouterLink>
    </div>

    <section id="about" class="py-5">
        <div class="container">
            <h2 class="text-center">{{ t('home.aboutTitle') }}</h2>
            <p class="text-center">{{ t('home.aboutContent1') }}</p>
            <p class="text-center">{{ t('home.aboutContent2') }}</p>
        </div>
    </section>

    <section id="features" class="bg-light py-5">
        <div class="container">
            <h2 class="text-center">{{ t('home.featuresTitle') }}</h2>
            <div class="row d-flex justify-content-center mt-4 mb-4">
                <div class="col-lg-6">
                    <div class="card">
                        <ul class="list-group list-group-flush">
                            <li v-for="feature in tm('home.featuresList')"
                                class="list-group-item d-flex align-items-center">
                                <div>
                                    <p style="margin-bottom: 5px;"><b>{{ feature.title }}</b></p>
                                    <p class="mb-0 text-muted">{{ feature.description }}</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import { useI18n } from 'vue-i18n';
const { t, tm } = useI18n();
</script>
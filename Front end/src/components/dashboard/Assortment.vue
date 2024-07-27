<template>
    <h6>{{ t('dashboard.assortment.title') }}</h6>
    <hr>
    <div class="accordion" id="categoriesAccordion">
        <!-- Categories btns -->
        <div class="d-flex">
            <div class="btn-group btn-group-sm flex-grow-1">
                <button type=" button" class="btn btn btn-success" data-bs-toggle="modal"
                    data-bs-target="#addCategoryModal"
                    :style="categories.length ? 'border-bottom-left-radius: 0;' : ''">{{
        t('general.addBtnText') }}</button>
                <button type="button" class="btn btn btn-warning" data-bs-toggle="modal"
                    data-bs-target="#editCategoryModal">{{
        t('general.editBtnText') }}</button>
                <button type="button" class="btn btn btn-danger"
                    :style="categories.length ? 'border-bottom-right-radius: 0;' : ''" data-bs-toggle="modal"
                    data-bs-target="#deleteCategoryModal" :disabled="safetyMode">{{
        t('general.delBtnText') }}</button>
            </div>
        </div>
        <!-- Categories -->
        <div v-for="category in categories" class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                    :data-bs-target="'#collapseCategory' + category">
                    {{ category }}
                </button>
            </h2>
            <div :id="'collapseCategory' + category" class="accordion-collapse collapse"
                data-bs-parent="#categoriesAccordion">
                <div class="d-flex">
                    <!-- Product addition btn -->
                    <button class="btn btn-sm btn-outline-success flex-grow-1 opacity-75" data-bs-toggle="modal"
                        data-bs-target="#newProductModal" :data-category="category"
                        style="border-top-left-radius: 0; border-top-right-radius: 0;">+</button>
                </div>
                <div class="accordion-body">
                    <div class="row g-2 align-items-center justify-content-center">
                        <!-- Products -->
                        <div class="col-auto"
                            v-for="product in goodsData.find(categoryObj => categoryObj.name === category).goods">
                            <div class="card">
                                <div class="card-header text-center">
                                    {{ product.name }}
                                </div>
                                <ul class="list-group list-group-flush text-center">
                                    <li class="list-group-item">
                                        <div>
                                            <ActionButtons :delDisabled="safetyMode" editModalId="#editProductModal"
                                                delModalId="#delProductModal" :data-name="product.name"
                                                :data-product-id="product.id" />
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <ProductAddition />
    <ProductEditing />
    <ProductDeletion />

    <CategoryAddition />
    <CategoryEditing />
    <CategoryDeletion />
</template>

<script setup>
import { computed } from 'vue';
import { useGoodsStore } from '../../stores/goods';
import { useSettingsStore } from '@/stores/settings';

import ActionButtons from '../table_elements/ActionButtons.vue';

import ProductAddition from './assortmentComponents/ProductAddition.vue'
import ProductEditing from './assortmentComponents/ProductEditing.vue'
import ProductDeletion from './assortmentComponents/ProductDeletion.vue'

import CategoryAddition from './assortmentComponents/CategoryAddition.vue'
import CategoryEditing from './assortmentComponents/CategoryEditing.vue'
import CategoryDeletion from './assortmentComponents/CategoryDeletion.vue'

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const categories = computed(() => useGoodsStore().categoriesNames)
const goodsData = computed(() => useGoodsStore().goodsData)
const safetyMode = computed(() => useSettingsStore().settingsData.goodsSafetyMode === "true" ? true : false);
</script>

<style scoped>
.accordion-item .accordion-button:focus {
    outline: none;
    box-shadow: none;
}

.accordion-item .accordion-button:not(.collapsed) {
    background-color: #F8F8F8;
    color: #212529;
}

.accordion-item .accordion-button:hover {
    background-color: #F8F8F8;
}
</style>
<template>
    <h6>ВАШ АСОРТИМЕНТ</h6>
    <hr>
    <div class="accordion" id="categoriesAccordion">
        <div class="d-flex">
            <div class="btn-group btn-group-sm flex-grow-1">
                <button type=" button" class="btn btn btn-success" data-bs-toggle="modal"
                    data-bs-target="#addCategoryModal" style="border-bottom-left-radius: 0;">Додати</button>
                <button type="button" class="btn btn btn-warning" data-bs-toggle="modal"
                    data-bs-target="#editCategoryModal">Змінити</button>
                <button type="button" class="btn btn btn-danger" style="border-bottom-right-radius: 0;"
                    data-bs-toggle="modal" data-bs-target="#deleteCategoryModal">Видалити</button>
            </div>
        </div>
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
                    <button class="btn btn-sm btn-outline-success flex-grow-1 opacity-75" data-bs-toggle="modal"
                        data-bs-target="#newProductModal" :data-category="category"
                        style="border-top-left-radius: 0; border-top-right-radius: 0;">+</button>
                </div>
                <div class="accordion-body">
                    <div class="row align-items-center">
                        <div class="col-md-4"
                            v-for="product in goodsData.filter(productObj => productObj.category === category)">
                            <div class="card mb-3">
                                <div class="card-header text-center">
                                    {{ product.product }}
                                </div>
                                <ul class="list-group list-group-flush text-center">
                                    <li class="list-group-item">
                                        <div style="overflow: auto;">
                                            <ActionButtons editModalId="#editProductModal" delModalId="#delProductModal"
                                                :data-name="product.product" :data-product-id="product.id"
                                                style="display: flex; justify-content: center;" />
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
import { ref, computed, onMounted, watch } from 'vue';
import { useGoodsStore } from '../../stores/goods';
import ActionButtons from '../table_elements/ActionButtons.vue';

import ProductAddition from './assortmentControls/ProductAddition.vue'
import ProductEditing from './assortmentControls/ProductEditing.vue'
import ProductDeletion from './assortmentControls/ProductDeletion.vue'

import CategoryAddition from './assortmentControls/CategoryAddition.vue'
import CategoryEditing from './assortmentControls/CategoryEditing.vue'
import CategoryDeletion from './assortmentControls/CategoryDeletion.vue'

const categories = computed(() => useGoodsStore().categoriesNames)
const goodsData = computed(() => useGoodsStore().inStockGoodsData)
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
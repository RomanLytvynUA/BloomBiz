<template>
    <div class="modal fade" id="editCategoryModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('dashboard.assortment.categories.editionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="editCategoryForm">
                        <CategoriesInput ref="targetCategoryInput" :customOption="false"
                            :label="t('dashboard.assortment.categories.categoryLabel')"
                            @category-changed="(category) => editCategoryInput.customCategoryInput = category"
                            @units-changed="(units) => editCategoryInput.categoryUnits = units" />
                        <CategoriesInput ref="editCategoryInput"
                            :label="t('dashboard.assortment.categories.changedCategoryLabel')" :custom="true" />
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-warning" @click.prevent="validateCategory()">{{
                        t('general.saveBtnText') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import CategoriesInput from '../../form_elements/CategoriesInput.vue';
import { useGoodsStore } from '../../../stores/goods';
import { ref } from 'vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const editCategoryInput = ref(null)
const targetCategoryInput = ref(null)

function validateCategory() {
    let valid = true
    const form = document.getElementById('editCategoryForm')

    // add 'is-invalid' class to every element of <form> where there is no value
    for (const element of form.elements) {
        if (element.tagName === 'INPUT' && !element.value && element.name !== 'additional') {
            element.classList.add('is-invalid');
            valid = false
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid) {
        const categoryData = new FormData(form)

        let json = {}
        json.targetCategory = targetCategoryInput.value.categorySelect
        categoryData.forEach((value, key) => {
            json[key] = value;
        });

        $(document.getElementById('editCategoryModal')).modal('hide');
        useGoodsStore().editCategory(json);
        form.reset();
        targetCategoryInput.value.reset();
    }
}

</script>

<style scoped>
.modal-body :last-child {
    margin-bottom: 0 !important;
}

.modal-footer {
    padding: 0;
}

.modal-footer>button {
    width: 100%;
    height: 100%;
    margin: 0;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
</style>
<template>
    <div class="modal fade" id="addCategoryModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('dashboard.assortment.categories.additionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="newCategoryForm">
                    <div class="modal-body">
                        <CategoriesInput ref="categoryInput" :label="t('dashboard.assortment.categories.categoryLabel')"
                            :custom="true" />
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-success" @click.prevent="validateCategory()">{{
                        t('general.addBtnText') }}</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import CategoriesInput from '../../form_elements/CategoriesInput.vue';
import { useGoodsStore } from '../../../stores/goods';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

function validateCategory() {
    let valid = true
    const form = document.getElementById('newCategoryForm')

    // add 'is-invalid' class to every element of <form> that has no value
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
        categoryData.forEach((value, key) => {
            json[key] = value;
        });

        $(document.getElementById('addCategoryModal')).modal('hide');
        useGoodsStore().createCategory(json);
        form.reset();
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
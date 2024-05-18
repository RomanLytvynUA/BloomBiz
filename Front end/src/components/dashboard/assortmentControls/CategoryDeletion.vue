<template>
    <div class="modal fade" id="deleteCategoryModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Видалення категорію</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="delCategoryForm">
                        <CategoriesInput :customOption="false" />
                        <div class="input-group mb-3">
                            <div class="input-group-text">
                                <input class="form-check-input mt-0" type="checkbox">
                            </div>
                            <textarea class="form-control" ref="warningTextArea"
                                value="Я розумію що категорія і всі пов'язані з нею товари будуть видалені."
                                readonly></textarea>
                        </div>

                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                    <button type="submit" class="btn btn-danger" @click.prevent="validateCategory()">Зберегти</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import CategoriesInput from '../../form_elements/CategoriesInput.vue'
import { ref } from 'vue';
import { useGoodsStore } from '../../../stores/goods';

const warningTextArea = ref(null)

function validateCategory() {
    let valid = true
    const form = document.getElementById('delCategoryForm')

    // add 'is-invalid' class to every element of <form> where there is no value
    for (const element of form.elements) {
        if (!element.disabled && (!element.value || (element.type === 'checkbox' && !element.checked)) && element.tagName !== 'TEXTAREA') {
            element.classList.add('is-invalid');
            valid = false;
        } else {
            element.classList.remove('is-invalid');
        }
    }

    if (valid) {
        const categoryData = new FormData(form)
        const selectedId = useGoodsStore().goodsData.find(category => category.name === categoryData.get("category")).id

        $(document.getElementById('deleteCategoryModal')).modal('hide');
        useGoodsStore().delCategory(selectedId);
        form.reset();
        warningTextArea.value.value = "Я розумію що категорія і всі пов'язані з нею товари будуть видалені."
    }
}

</script>
<template>
    <div class="modal fade" id="newProductModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('dashboard.assortment.products.additionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form id="newProductForm">
                    <div class="modal-body">
                        <InputField :label="t('dashboard.assortment.products.nameLabel')" type="text" name="product" />
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-success" @click.prevent="validateProduct()">{{
                        t('general.addBtnText') }}</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import InputField from '../../form_elements/InputField.vue';
import { useGoodsStore } from '../../../stores/goods';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const category = ref(null);

onMounted(() => {
    const modalElement = document.getElementById('newProductModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        category.value = btn.getAttribute('data-category');
    });
});

function validateProduct() {
    let valid = true
    const form = document.getElementById('newProductForm')

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
        const data = new FormData(form)
        let json = {}
        json.category = category.value
        data.forEach((value, key) => {
            json[key] = value;
        });

        $(document.getElementById('newProductModal')).modal('hide');
        useGoodsStore().createProduct(json);
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
<template>
    <div class="modal fade" id="delExpenseModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t('expenses.deletionModalTitle') }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>{{ t('expenses.deletionModalConfirmationMessage') }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteExpense()">{{
                        t('general.delBtnText') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useExpensesStore } from '@/stores/expenses';

const expensesStore = useExpensesStore();
const selectedExpenseId = ref(null);

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

onMounted(() => {
    const modalElement = document.getElementById('delExpenseModal');
    modalElement.addEventListener('show.bs.modal', (event) => {
        const btn = event.relatedTarget;
        selectedExpenseId.value = btn.parentElement.getAttribute('data-expense-id');
    });
});

function deleteExpense() {
    expensesStore.delExpense(selectedExpenseId.value);
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
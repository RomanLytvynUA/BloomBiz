<template>
    <div class="modal fade" id="delExpenseModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title">Ви впевненні?</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Також зі складу будуть видалені всі товари, що пов'язані з цією витратою. Цю дію не можна відмінити.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteExpense()">Видалити</button>
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
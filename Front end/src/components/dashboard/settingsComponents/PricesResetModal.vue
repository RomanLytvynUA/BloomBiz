<template>
    <div class="modal fade" id="pricesResetModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Скинути ціни</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Всі ціни, що ви змінили будуть перераховані спираючись на націнку за змовченням. Цю дію не можна
                    відмінити.
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                    <button type="submit" class="btn btn-danger" data-bs-dismiss="modal" @click.prevent="">Скинути</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
</script>
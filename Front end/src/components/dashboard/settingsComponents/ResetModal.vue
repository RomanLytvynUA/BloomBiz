<template>
    <div class="modal fade" id="resetModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Скинути налаштування</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Всі налаштування будуть встановленні за змовченням.
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Скасувати</button>
                    <button type="submit" class="btn btn-danger" data-bs-dismiss="modal"
                        @click.prevent="$emit('reset')">Скинути</button>
                </div>
            </div>
        </div>
    </div>
</template>
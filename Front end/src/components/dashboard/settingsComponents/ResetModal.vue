<template>
    <div class="modal fade" id="resetModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ t("dashboard.settings.resetModalTitle") }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    {{ t("dashboard.settings.resetModalConfirmationMessage") }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{
                        t("general.cancelBtnText") }}</button>
                    <button type="submit" class="btn btn-danger" data-bs-dismiss="modal"
                        @click.prevent="$emit('reset')">{{
                        t("general.resetBtnText") }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>
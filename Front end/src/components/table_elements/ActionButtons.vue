<template>
    <div class="btn-group btn-group-sm" style="min-width: 190px;" role="group">
        <button style="width: 50%;" ref="tooltipButton" type="button" class="btn btn-sm btn-outline-danger opacity-75"
            :data-toggle="delDisabled ? 'tooltip' : ''"
            :title="delDisabled ? 'Функція не доступна, перевірте налаштування.' : ''"
            :data-bs-toggle="!delDisabled ? 'modal' : ''" :data-bs-target="delModalId">{{ delText ||
                $t('general.delBtnText') }}</button>
        <button style="width: 50%;" type="button" class="btn btn-sm btn-outline-success opacity-75"
            data-bs-toggle="modal" :data-bs-target="editModalId">{{
                editText || $t('general.editBtnText') }}</button>
    </div>
</template>

<script>
export default {
    props: {
        delModalId: String,
        editModalId: String,
        delDisabled: Boolean,
        delText: {
            type: String
        },
        editText: {
            type: String
        },
    },
    mounted() {
        $('[data-toggle="tooltip"]').click(function () {
            $(this).tooltip('show');
            $(this).mouseleave(function () {
                $(this).tooltip('dispose');
            });
        });
    }
}
</script>

<style scoped>
.btn[data-toggle="tooltip"] {
    cursor: not-allowed;
    opacity: 50% !important;
}

.btn[data-toggle="tooltip"]:hover {
    background-color: var(--bs-btn-bg);
    color: var(--bs-btn-color);
}
</style>
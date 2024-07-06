<template>
    <div class="btn-group btn-group-sm justify-content-center" role="group">
        <button ref="tooltipButton" type="button" class="btn btn-sm btn-outline-danger opacity-75"
            :data-toggle="delDisabled ? 'tooltip' : ''"
            :title="delDisabled ? 'Функція не доступна, перевірте налаштування.' : ''"
            :data-bs-toggle="!delDisabled ? 'modal' : ''" :data-bs-target="delModalId">{{ delText }}</button>
        <button type="button" class="btn btn-sm btn-outline-success opacity-75" data-bs-toggle="modal"
            :data-bs-target="editModalId">{{ editText }}</button>
    </div>
</template>

<script>
export default {
    props: {
        delModalId: String,
        editModalId: String,
        delDisabled: Boolean,
        delText: {
            type: String,
            default: 'Видалити'
        },
        editText: {
            type: String,
            default: 'Редагувати'
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
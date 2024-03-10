<template>
    <div class="btn-group btn-group-sm justify-content-center" role="group">
        <button type="button" class="btn btn-sm btn-outline-danger opacity-75"
        data-bs-toggle="modal"
        :data-bs-target="delModalId"    
        >{{ delText }}</button>
        <button type="button" class="btn btn-sm btn-outline-success opacity-75"
        data-bs-toggle="modal"
        :data-bs-target="editModalId"  
        >{{ editText }}</button>
    </div>
</template>

<script>
export default {
    props: {
        delModalId: String,
        editModalId: String,
        delText: {
            type: String,
            default: 'Видалити'
        },
        editText: {
            type: String,
            default: 'Редагувати'
        },
    }
}
</script>
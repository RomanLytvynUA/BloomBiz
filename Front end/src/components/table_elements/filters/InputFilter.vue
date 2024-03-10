<template>
    <div class="mb-3">
        <input v-model="filter" class="form-control form-control-sm" type="text" :placeholder="placeholder">
    </div>
</template>

<script>
export default {
    props: {
        placeholder: String,    
    },
    data() {
        return {
            filter: '',
        };
    },
    methods: {
        filterData(data) {
            return this.filter === '' || data.toLowerCase().replace(/\s/g, '').includes(this.filter.toLowerCase().replace(/\s/g, ''));
        },
    },
    watch: {
        filter() {
            this.$emit('filterChanged');
        }
    }
};
</script>

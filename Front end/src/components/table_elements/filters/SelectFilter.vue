<template>
    <div class="mb-3">
        <select v-model="filter" class="form-select form-select-sm">
            <option :value="!defaultText ? 'all' : defaultText" style="background-color: green;">{{ !defaultText ?
            $t('general.allSelectOption') : defaultText }}</option>
            <option v-for="option in options" :value="option">{{ option }}</option>
        </select>
    </div>
</template>

<script>
export default {
    props: {
        options: Array,
        defaultText: {
            type: String,
            default: "",
        },

    },
    data() {
        return {
            filter: !this.defaultText ? 'all' : this.defaultText,
        };
    },
    methods: {
        filterData(data) {
            return this.filter === 'all' || this.filter === data
        },
        getChoice() {
            return this.filter
        },
    },
    watch: {
        filter() {
            this.$emit('filterChanged');
        },
        options() {
            this.filter = !this.defaultText ? 'all' : this.defaultText;
        }
    }
};
</script>

<template>
    <div class="input-group input-group-sm mb-3">
        <span class="input-group-text">Від </span>
        <input ref="fromDateFilter" type="date" class="form-control" :value="firstDayOfMonthDate" @input="$emit('filterChanged')">
        <span class="input-group-text"> до </span>
        <input ref="toDateFilter" type="date" class="form-control" :value="lastDayOfMonthDate" @input="$emit('filterChanged')">
    </div>
</template>

<script>
export default {
    data() {
        return {
            firstDayOfMonthDate: new Date().toISOString().slice(0, 7) + '-01',
            lastDayOfMonthDate: new Date(new Date().getFullYear(), new Date().getMonth() + 1, 1).toISOString().split('T')[0],
            fromDateFilter: null,
            toDateFilter: null,
        };
    },
    methods: {
        filterDate(rawDate) {
            this.fromDateFilter = new Date(this.$refs.fromDateFilter.value);
            this.toDateFilter = new Date(this.$refs.toDateFilter.value);

            const date = new Date(rawDate);

            return (this.fromDateFilter <= date || this.fromDateFilter == 'Invalid Date') && (date <= this.toDateFilter || this.toDateFilter == 'Invalid Date')
        },
    },
};
</script>

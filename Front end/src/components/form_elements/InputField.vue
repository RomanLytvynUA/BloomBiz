<template>
    <div class="mb-3">
        <label class="form-label">{{ label }}</label>
        <input class="form-control" v-model="inputValue" :type="type" :name="name">
    </div>
</template>

<script>
export default {
    props: ['label', 'name', 'type', 'value'],
    data() {
        return {
            inputValue: this.value,
        };
    },
    watch: {
        value(newVal) {
            this.inputValue = newVal;
        },
    },
    methods: {
        reset() {
            this.inputValue = this.value;
        },
    },
};
</script>

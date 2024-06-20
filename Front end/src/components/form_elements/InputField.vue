<template>
    <div :class="divClasses">
        <label class="form-label">{{ label }}</label>
        <input class="form-control" v-model="inputValue" :type="type" :name="name" :disabled="disabled">
    </div>
</template>

<script>
export default {
    props: {
        'label': String,
        'name': String,
        'type': String,
        'value': String,
        'disabled': Boolean,
        'divClasses': {
            type: String,
            default: "mb-3"
        }
    },
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

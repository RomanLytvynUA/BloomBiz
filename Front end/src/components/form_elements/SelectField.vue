<template>
    <label v-if="label" class="form-label">{{ label }}</label>
    <div :class="divClasses">
        <select ref="selectElement" v-if="!customOption" :name="name" v-model="select" class="form-select">
            <option v-if="preselectedValue && !options.includes(preselectedValue)" :value="preselectedValue">{{
        preselectedValue }}</option>
            <option v-if="customOptionValue" :value="customOptionValue" style="background-color: green;">{{
        customOptionValue }}</option>
            <option v-for="option in options" :value="option.value ? option.value : option">{{ option.name ? option.name
        : option }}</option>
        </select>
        <input v-if="customOption" v-model="customInput" class="form-control" :name="name">
    </div>
</template>

<script>
export default {
    props: {
        label: String,
        name: String,
        options: Array,
        customOptionValue: String,
        preselectedValue: {},
        divClasses: {
            type: String,
            default: "mb-3"
        },
    },
    emits: ['valueSelected'],
    data() {
        return {
            select: this.preselectedValue,
            customInput: '',
            customOption: false,
        };
    },
    methods: {
        reset() {
            this.customOption = false
            this.select = this.preselectedValue
            this.customInput = ''
        }
    },
    watch: {
        select() {
            if (this.select === this.customOptionValue) {
                this.customOption = true
            } else {
                this.$emit('valueSelected', this.select)
            }
        },
        customInput() {
            this.$emit('valueSelected', this.customInput)
        },
        preselectedValue() {
            this.select = this.preselectedValue
        }
    }
};
</script>

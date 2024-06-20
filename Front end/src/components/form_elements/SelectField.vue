<template>
    <div :class="divClasses">
        <label v-if="label" class="form-label">{{ label }}</label>
        <select ref="selectElement" v-if="!customOption" :name="name" v-model="select" :disabled="disabled"
            class="form-select">
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
        directCustomOption: {
            type: Boolean,
            default: false
        },
        disabled: {
            type: Boolean,
            default: false
        },
        preselectedValue: {},
        divClasses: {
            type: String,
            default: "mb-3"
        },
    },
    emits: ['valueSelected', 'customOptionSelected'],
    data() {
        return {
            select: this.preselectedValue,
            customInput: '',
            customOption: this.directCustomOption,
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
                this.$emit('customOptionSelected', this.select)
            } else {
                this.$emit('valueSelected', this.select)
            }
        },
        directCustomOption() {
            // Watch for prop change to force custom input
            this.customOption = this.directCustomOption
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

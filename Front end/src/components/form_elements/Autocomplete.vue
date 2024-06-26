<template>
    <div :class="divClasses">
        <div class="dropdown">
            <label v-if="label" class="form-label">{{ label }}</label>
            <input ref="inputElement" :disabled="disabled" v-model="input" autocomplete="off" :class="{
        'form-control': customOption, 'form-select': !customOption,
        'form-control-sm': customOption && small, 'form-select-sm': !customOption && small,
    }" data-bs-toggle="dropdown" :name="name" data-bs-offset="0,0" :style="dropdownOpened && !customOption ?
        'border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;' :
        'border-bottom-left-radius: 4px; border-bottom-right-radius: 4px;'">
            <ul v-show="!customOption" class="dropdown-menu" ref="dropdownMenu">
                <li>
                    <button v-if="customOptionLabel"
                        :class="small ? 'dropdown-item small-btn' : 'dropdown-item normal-btn'"
                        @click.prevent="customOption = true; dropdownOpened = false; $emit('customOptionSelected')"
                        style="background-color: green;">
                        {{ customOptionLabel }}
                    </button>
                </li>
                <li>
                    <button v-for="option in filteredOptions"
                        @click.prevent="input = option; emit('valueSelected', option); dropdownOpened = false"
                        :class="small ? 'dropdown-item small-btn' : 'dropdown-item normal-btn'">
                        {{ option }}
                    </button>
                </li>
                <li v-if="!filteredOptions.length" class="text-center">Нічого не знайдено.</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, defineEmits } from 'vue';

const props = defineProps({
    label: String,
    name: String,
    options: Array,
    customOptionLabel: {
        type: String,
        default: "+ Додати нового"
    },
    preselectedValue: {
        type: String,
        default: ""
    },
    forceCustomInput: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    },
    small: {
        type: Boolean,
        default: false
    },
    divClasses: {
        type: String,
        default: "mb-3"
    },
})
const emit = defineEmits(['valueSelected', 'customOptionSelected']);

const inputElement = ref('');
const input = ref(props.preselectedValue);
watch(() => input.value, () => customOption.value ? emit('valueSelected', input.value) : {})
watch(() => props.preselectedValue, () => input.value = props.preselectedValue)

const customOption = ref(props.forceCustomInput);
watch(() => props.forceCustomInput, () => { customOption.value = props.forceCustomInput; dropdownOpened.value = false; })
const dropdownMenu = ref(null);
const dropdownOpened = ref(false);

const filteredOptions = computed(() => {
    return String(input.value).length ? props.options.filter(option => String(option).toLocaleLowerCase().includes(input.value.toLocaleLowerCase())) : props.options
})


const reset = () => {
    input.value = '';
    customOption.value = false;
}

onMounted(() => {
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.attributeName === 'class') {
                dropdownOpened.value = dropdownMenu.value.classList.contains('show');
                props.options.includes(input.value) || customOption.value ? {} : input.value = ''
            }
        });
    });

    observer.observe(dropdownMenu.value, { attributes: true });
});
defineExpose({ input, inputElement, reset })
</script>

<style scoped>
.dropdown-menu {
    max-height: 300px;
    overflow-y: auto;
    overflow-x: auto;
    width: 100%;
    padding: 0;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

.dropdown-item:focus {
    background-color: #F8F9FA;
    color: black;
}

.form-select:focus {
    outline: none !important;
    border-color: #dee2e6;
    box-shadow: none !important;
}

.small-btn {
    padding: 3px;
}

.normal-btn {
    padding: 5px;
}

.form-select:hover {
    cursor: default;
}
</style>
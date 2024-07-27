<template>
    <div class="accordion" style="margin-bottom: 6px;" :id="name + 'Accordion'">
        <div class="accordion-item">
            <h2 class="accordion-header">
                <!-- Header  -->
                <button style="padding: 8px 12px 8px 12px;" class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse" :data-bs-target="'#' + name + 'Options'"
                    :data-bs-parent="'#' + name + 'Accordion'">
                    <!-- Description  -->
                    <span class="d-block w-100">
                        <p style="margin: 0px 0px 5px 0px;">{{ title }}</p>
                        <p class="text-muted mb-0" style="display: block;">{{ info }}</p>
                    </span>
                </button>
            </h2>
            <div :id="name + 'Options'" class="accordion-collapse collapse" :data-bs-parent="'#' + name + 'Accordion'">
                <!-- Addition btn -->
                <div class="d-flex">
                    <button class="btn btn-sm btn-outline-success flex-grow-1 opacity-75" data-bs-toggle="modal"
                        :data-bs-target="'#' + additionModalId" :data-category="category"
                        style="border-top-left-radius: 0; border-top-right-radius: 0;">+</button>
                </div>
                <div class="accordion-body">
                    <!-- Content -->
                    <div class="row align-items-center justify-content-center">
                        <div class="col-auto d-flex justify-content-center" v-for="value in options">
                            <div class="input-group input-group-sm">
                                <span class="input-group-text">{{ value }}</span>
                                <button class="btn btn-danger" type="button"
                                    @click="options.splice(options.indexOf(value), 1); $emit('optionDeleted')">X</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue';

const emit = defineEmits(['optionDeleted'])
const props = defineProps({
    name: String,
    title: String,
    info: String,
    values: Array,
    additionModalId: String,
})
const options = ref(props.values)

watch(
    () => props.values,
    (newValue, oldValue) => {
        options.value = newValue;
    }
);
</script>

<style scoped>
.accordion-item .accordion-button:focus {
    outline: none;
    box-shadow: none;
}

.accordion-item .accordion-button:not(.collapsed) {
    background-color: #F8F8F8;
    color: #212529;
}

.accordion-item .accordion-button:hover {
    background-color: #F8F8F8;
}
</style>
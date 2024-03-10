<template>
    <a tabindex="0" 
    :class="'popover-dismiss'+id" 
    data-bs-toggle="popover" 
    data-bs-trigger="focus" 
    :data-bs-title="title" 
    :data-bs-content="text"
    data-bs-placement="bottom"
    style="cursor: pointer; text-decoration: underline;"
    >{{ trancatedText }}</a>
</template>

<script setup>
import { onMounted, computed } from 'vue';

const props = defineProps(['maxSize', 'text', 'title', 'id']);

const trancatedText = computed(() => {
    if (props.text.length > props.maxSize) {
        return `${props.text.slice(0, props.maxSize)}...`
    } else {
        return props.text
    }
})

onMounted(() => {
    const popover = new bootstrap.Popover(document.querySelector(`.popover-dismiss${props.id}`), {
        trigger: 'focus'
    });
});
</script>
  
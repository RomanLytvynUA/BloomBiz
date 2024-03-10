<template>
    <div class="input-group input-group-sm m-3">
        <span class="input-group-text">{{text1}}</span>
        <div class="input-group-text">
            <input v-model="pickedRadio" class="form-check-input" type="radio" value="0" checked>
        </div>
        <span class="input-group-text">{{text2}}</span>
        <div class="input-group-text">
            <input v-model="pickedRadio" class="form-check-input" type="radio" value="1">
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            pickedRadio: new Date().toISOString().slice(0, 7) + '-01',
        };
    },
    props: {
        text1: String,
        text2: String,
    },
    methods: {
        getCheked() {
            return this.pickedRadio
        }
    }
}
</script>

<style scoped>
.input-group-text:not(span) {
    background-color: white;
}
</style>
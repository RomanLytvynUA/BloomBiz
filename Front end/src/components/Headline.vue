<template>
    <br>
    <h3 class="text-center display-6">{{ title }}</h3>
    <hr>
    <div class="text-center">
        <p style="color:#808080">{{ description }}</p>
    </div>
</template>

<script>
export default {
    props: [ 'title', 'description'],
}
</script>
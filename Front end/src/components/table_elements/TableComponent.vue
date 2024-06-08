<template>
    <div class="container table-responsive text-center">
        <table class="table table-sm align-middle" :style="`width: ${width}; margin: auto;`">
            <thead>
                <tr style="border: none;">
                    <th v-for="filter in filters" style="border: none;">
                        <component :is="filter.component" v-bind="filter.props" :ref="filter.reference"
                            @filterChanged="$emit('filterChanged')"></component>
                    </th>
                </tr>
                <tr class="table-light rounded-top" style="border-radius:10px 0 0 10px">
                    <th v-for="header in headers" :key="header" scope="col" :width="header.size">{{ header.name }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in rows" :key="row">
                    <td v-for="data in row">
                        <!-- Check if the data is an object with a 'component' property -->
                        <component v-if="typeof data === 'object' && data.component" :is="data.component"
                            v-bind="data.props"></component>
                        <!-- If not an object, just display the data -->
                        <template v-else>{{ data }}</template>
                    </td>
                </tr>
            </tbody>
        </table>
        <br>
        <h6 v-show="!rows.length">
            Данних, що збігаються з вашим запитом не знайдено ¯\_(ツ)_/¯
        </h6>
    </div>
</template>

<script>
export default {
    props: {
        headers: Array,
        rows: Array,
        filters: Array,
        width: {
            default: '85%',
            type: String
        }
    },
}
</script>
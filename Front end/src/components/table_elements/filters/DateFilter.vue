<template>
    <div>
        <div v-if="type === 'year' || type === 'quarter'" class="input-group input-group-sm flex-nowrap"
            :class="{ 'mb-3': mb3 }">
            <span class="input-group-text">{{ $t('general.dateFilterFrom') }} </span>
            <select ref="fromYearFilter" class="form-select" @input="$emit('filterChanged')">
                <option v-for="i in 10" :selected="type === 'quarter' ? i === 1 : i === 10"
                    :value="new Date().getFullYear() - i + 1">{{ new
            Date().getFullYear() - i + 1 }}
                </option>
            </select>
            <span class="input-group-text"> {{ $t('general.dateFilterTo') }} </span>
            <select ref="toYearFilter" class="form-select" @input="$emit('filterChanged')">
                <option v-for="i in 11" :selected="i === 0" :value="new Date().getFullYear() - i + 1">{{ new
            Date().getFullYear() - i + 1 }}
                </option>
            </select>
        </div>
        <div v-else class="input-group input-group-sm flex-nowrap" :class="{ 'mb-3': mb3 }">
            <span class="input-group-text">{{ $t('general.dateFilterFrom') }} </span>
            <input ref="fromDateFilter" :type="type === 'day' ? 'date' : type" class="form-control"
                :value="firstDefaultDate" @input="$emit('filterChanged')">
            <span class="input-group-text"> {{ $t('general.dateFilterTo') }} </span>
            <input ref="toDateFilter" :type="type === 'day' ? 'date' : type" class="form-control"
                :value="lastDefaultDate" @input="$emit('filterChanged')">
        </div>
    </div>
</template>


<script>
import { format, startOfMonth, endOfMonth, startOfWeek, endOfWeek, getWeek, getYear, isAfter, isBefore, isEqual, startOfDay, endOfYear, endOfDay } from 'date-fns';

export default {
    props: {
        type: {
            default: 'date'
        },
        mb3: {
            default: true
        },
    },
    data() {
        return {
            firstDefaultDate: this.getDefaultFromDate(),
            lastDefaultDate: this.getDefaultToDate(),
            fromDateFilter: null,
            toDateFilter: null,
            fromYearFilter: null,
            toYearFilter: null,
        };
    },
    watch: {
        type() {
            this.firstDefaultDate = this.getDefaultFromDate()
            this.lastDefaultDate = this.getDefaultToDate()
            this.$nextTick(() => {
                this.$emit('filterChanged')
            });
        },
    },
    methods: {
        filterDate(rawDate) {
            switch (this.type) {
                case 'date':
                    this.fromDateFilter = new Date(this.$refs.fromDateFilter.value);
                    this.toDateFilter = new Date(this.$refs.toDateFilter.value);
                    return (
                        (isAfter(startOfDay(rawDate), startOfDay(this.fromDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.fromDateFilter)) || this.fromDateFilter == 'Invalid Date') &&
                        (isBefore(startOfDay(rawDate), startOfDay(this.toDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.toDateFilter)) || this.toDateFilter == 'Invalid Date')
                    );
                case 'day':
                    this.fromDateFilter = new Date(this.$refs.fromDateFilter.value);
                    this.toDateFilter = new Date(this.$refs.toDateFilter.value);
                    return (
                        (isAfter(startOfDay(rawDate), startOfDay(this.fromDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.fromDateFilter))) &&
                        (isBefore(startOfDay(rawDate), startOfDay(this.toDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.toDateFilter)))
                    );
                case 'week':
                    this.fromDateFilter = this.$refs.fromDateFilter.value;
                    this.toDateFilter = this.$refs.toDateFilter.value;

                    const [startYear, startWeek] = this.fromDateFilter.split('-W');
                    const [endYear, endWeek] = this.toDateFilter.split('-W');

                    this.fromDateFilter = new Date(startYear, 0, (parseInt(startWeek) - 1) * 7 + 1);
                    this.toDateFilter = new Date(endYear, 0, (parseInt(endWeek) - 1) * 7 + 7);
                    return (
                        (isAfter(startOfDay(rawDate), startOfDay(this.fromDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.fromDateFilter))) &&
                        (isBefore(startOfDay(rawDate), endOfDay(this.toDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.toDateFilter)))
                    );
                case 'month':
                    this.fromDateFilter = new Date(this.$refs.fromDateFilter.value);
                    this.toDateFilter = new Date(this.$refs.toDateFilter.value);
                    return (
                        (isAfter(startOfDay(rawDate), startOfDay(this.fromDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.fromDateFilter))) &&
                        (isBefore(startOfDay(rawDate), endOfDay(this.toDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.toDateFilter)))
                    );
                case 'quarter':
                    this.fromDateFilter = new Date(this.$refs.fromYearFilter.value);
                    this.toDateFilter = endOfYear(new Date(this.$refs.toYearFilter.value));
                    return (
                        (isAfter(startOfDay(rawDate), startOfDay(this.fromDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.fromDateFilter))) &&
                        (isBefore(startOfDay(rawDate), endOfDay(this.toDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.toDateFilter)))
                    );
                case 'year':
                    this.fromDateFilter = new Date(this.$refs.fromYearFilter.value);
                    this.toDateFilter = endOfYear(new Date(this.$refs.toYearFilter.value));
                    return (
                        (isAfter(startOfDay(rawDate), startOfDay(this.fromDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.fromDateFilter))) &&
                        (isBefore(startOfDay(rawDate), endOfDay(this.toDateFilter)) || isEqual(startOfDay(rawDate), startOfDay(this.toDateFilter)))
                    );
            }
        },
        getDate() {
            switch (this.type) {
                case 'date':
                    return { fromDate: new Date(this.$refs.fromDateFilter.value), toDate: new Date(this.$refs.toDateFilter.value) };
                case 'day':
                    return { fromDate: new Date(this.$refs.fromDateFilter.value), toDate: new Date(this.$refs.toDateFilter.value) };
                case 'week':
                    return { fromDate: this.$refs.fromDateFilter.value, toDate: this.$refs.toDateFilter.value };
                case 'month':
                    return { fromDate: new Date(this.$refs.fromDateFilter.value), toDate: new Date(this.$refs.toDateFilter.value) };
                case 'quarter':
                    return { fromDate: new Date(this.$refs.fromYearFilter.value), toDate: new Date(this.$refs.toYearFilter.value) };
                case 'year':
                    return { fromDate: new Date(this.$refs.fromYearFilter.value), toDate: new Date(this.$refs.toYearFilter.value) };
                default:
                    return {};
            }
        },
        getDefaultFromDate() {
            const currentDate = new Date();
            switch (this.type) {
                case 'date':
                    return format(startOfMonth(currentDate), 'yyyy-MM-dd');
                case 'day':
                    return format(startOfWeek(currentDate, { weekStartsOn: 1 }), 'yyyy-MM-dd');
                case 'week':
                    return `${getYear(currentDate)}-W${getWeek(startOfMonth(currentDate), { weekStartsOn: 1 }).toString().padStart(2, '0')}`
                case 'month':
                    return getYear(new Date()) + '-01';
                default:
                    return '';
            }
        },
        getDefaultToDate() {
            const currentDate = new Date();
            switch (this.type) {
                case 'date':
                    return format(endOfMonth(currentDate), 'yyyy-MM-dd');
                case 'day':
                    return format(endOfWeek(currentDate, { weekStartsOn: 1 }), 'yyyy-MM-dd');
                case 'week':
                    return `${getYear(currentDate)}-W${getWeek(endOfMonth(currentDate), { weekStartsOn: 1 }).toString().padStart(2, '0')}`
                case 'month':
                    return getYear(new Date()) + '-12';
                default:
                    return '';
            }
        },
    },
};
</script>

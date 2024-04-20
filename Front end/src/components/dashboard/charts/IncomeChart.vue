<template>
    <div>
        <div class="row g-2 justify-content-center">
            <div class="col-auto d-flex align-items-center">
                <p>Статистика прибутку за </p>
            </div>
            <div class="col-auto">
                <select v-model="incomeChartTypeSelect" class="form-select form-select-sm">
                    <option value="day">День</option>
                    <option value="week">Тиждень</option>
                    <option value="month">Місяць</option>
                    <option value="quarter">Квартал</option>
                    <option value="year">Рік</option>
                </select>
            </div>
            <div class="col-auto">
                <DateFilter :type="incomeChartTypeSelect" ref="incomeChartDateSelect" @filterChanged="() => {
                    incomeChartObj.data.labels = getIncomeChartLabels(); incomeChartObj.update(); setIncomeChartData();
                }" />
            </div>
            <div class="col-auto">
                <button type="button" class="btn btn-sm btn-secondary" data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasFilters">Фільтри</button>
            </div>
        </div>
        <canvas ref="incomeChart"></canvas>
    </div>
    <div class="offcanvas offcanvas-end" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1"
        id="offcanvasFilters">
        <div class="offcanvas-header">
            <h4 class="offcanvas-title">Фільтри</h4>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <h5>Замовлення</h5>
            <h6>Статус</h6>
            <ul class="filter-ul">
                <li v-for="status in orderStatuses" :key="status">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" :value="status" :checked="status === 'Продано'"
                            @change=" filteredOrderStatuses.includes(status) ? filteredOrderStatuses.splice(filteredOrderStatuses.indexOf(status), 1) :
                    filteredOrderStatuses.push(status); setIncomeChartData()">
                        <label class="form-check-label">
                            {{ status }}
                        </label>
                    </div>
                </li>
            </ul>
            <h5>Витрити</h5>
            <h6>Постачальники</h6>
            <ul class="filter-ul">
                <li v-for="supplier in suppliers" :key="supplier">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" :value="supplier" checked @change=" filteredExpenseSuppliers.includes(supplier) ? filteredExpenseSuppliers.splice(filteredExpenseSuppliers.indexOf(supplier), 1) :
                    filteredExpenseSuppliers.push(supplier); setIncomeChartData()">
                        <label class="form-check-label">
                            {{ supplier }}
                        </label>
                    </div>
                </li>
            </ul>
            <h6>Категорії</h6>
            <ul class="filter-ul">
                <li v-for="category in categories" :key="category">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" :value="category" checked @change=" filteredExpenseCategories.includes(category) ? filteredExpenseCategories.splice(filteredExpenseCategories.indexOf(category), 1) :
                    filteredExpenseCategories.push(category); setIncomeChartData()">
                        <label class="form-check-label">
                            {{ category }}
                        </label>
                    </div>
                </li>
            </ul>
        </div>
    </div>
    <!-- <button @click="console.log(filteredOrderStatuses)">---</button> -->
</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { orderStatuses } from '../../../config';
import { useOrdersStore } from '../../../stores/orders';
import { useExpensesStore } from '../../../stores/expenses';
import { useGoodsStore } from '../../../stores/goods';
import { useSuppliersStore } from '../../../stores/suppliers';
import { eachWeekOfInterval, format, eachDayOfInterval, getMonth, getYear, addMonths, eachYearOfInterval, isEqual, endOfYear, startOfDay, isSameWeek, eachMonthOfInterval, isSameMonth, eachQuarterOfInterval, isSameQuarter, isSameYear } from 'date-fns';
import DateFilter from '../../table_elements/filters/DateFilter.vue';
import Chart from 'chart.js/auto';

let incomeChartObj = null
const incomeChart = ref(null);

const ordersData = computed(() => useOrdersStore().ordersData)
const expensesData = computed(() => useExpensesStore().expensesData)
const categories = computed(() => useGoodsStore().categoriesNames)
const categoriesData = computed(() => useGoodsStore().goodsData)
const suppliersData = computed(() => useSuppliersStore().suppliersData)
const suppliers = computed(() => useSuppliersStore().suppliersNames)

const filteredOrderStatuses = ['Продано']
const filteredExpenseCategories = [].concat(categories.value)
const filteredExpenseSuppliers = [].concat(suppliers.value)

const incomeChartDateSelect = ref(null);
const incomeChartTypeSelect = ref("day")

const getIncomeChartLabels = () => {
    const data = []
    const chartType = incomeChartTypeSelect.value
    const dateFilter = incomeChartDateSelect.value.getDate()
    let date = dateFilter.fromDate

    switch (chartType) {
        case 'day':
            eachDayOfInterval({ start: dateFilter.fromDate, end: dateFilter.toDate }).forEach(date => data.push(format(date, 'dd.MM.yyyy')))
            return data
        case 'week':
            const [startYear, startWeek] = dateFilter.fromDate.split('-W');
            const [endYear, endWeek] = dateFilter.toDate.split('-W');

            const startDate = new Date(startYear, 0, (parseInt(startWeek) - 1) * 7 + 1);
            const endDate = new Date(endYear, 0, (parseInt(endWeek) - 1) * 7 + 1);

            const weeksInRange = eachWeekOfInterval({ start: startDate, end: endDate }, { weekStartsOn: 1 });
            return weeksInRange.map(date => format(date, 'ww, yyyy'))
        case 'month':
            const months = ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень']
            while (date <= dateFilter.toDate) {
                data.push(`${months[getMonth(date)]} ${getYear(date)}`)
                date = addMonths(date, 1)
            }
            return data
        case 'quarter':
            eachYearOfInterval({ start: dateFilter.fromDate, end: dateFilter.toDate }).forEach(year => {
                data.push(`I, ${getYear(year)}`)
                data.push(`II, ${getYear(year)}`)
                data.push(`III, ${getYear(year)}`)
                data.push(`IV, ${getYear(year)}`)
            })
            return data
        case 'year':
            eachYearOfInterval({ start: dateFilter.fromDate, end: dateFilter.toDate }).forEach(year => {
                data.push(getYear(year))
            })
            return data
    }
};
const setIncomeChartData = () => {
    const chartType = incomeChartTypeSelect.value
    const dateFilter = incomeChartDateSelect.value.getDate()

    const orders = ordersData.value.filter(order => {
        return filteredOrderStatuses.includes(order.status) && incomeChartDateSelect.value.filterDate(order.date)
    });
    const expenses = expensesData.value.filter(expense => {
        const categoryName = categoriesData.value.find(category => category.id === expense.category).name
        const supplierName = suppliersData.value.find(supplier => supplier.id === expense.supplier).name
        return filteredExpenseCategories.includes(categoryName) && filteredExpenseSuppliers.includes(supplierName) && incomeChartDateSelect.value.filterDate(expense.date)
    });

    let expensesPrices = []
    let ordersPrices = []
    let incomePrices = []
    switch (chartType) {
        case 'day':
            eachDayOfInterval({ start: dateFilter.fromDate, end: dateFilter.toDate }).forEach(date => {
                const dayOrders = orders.filter(order => {
                    return isEqual(startOfDay(new Date(order.date)), startOfDay(date))
                })
                const dayExpenses = expenses.filter(expense => {
                    return isEqual(startOfDay(new Date(expense.date)), date)
                })
                const ordersPrice = dayOrders.reduce((total, order) => total + order.price, 0);
                const expensesPrice = dayExpenses.reduce((total, expense) => total + expense.total, 0);
                expensesPrices.push(expensesPrice)
                ordersPrices.push(ordersPrice)
                incomePrices.push(ordersPrice - expensesPrice)
            })
            break;
        case 'week':
            const [startYear, startWeek] = dateFilter.fromDate.split('-W');
            const [endYear, endWeek] = dateFilter.toDate.split('-W');
            const startDate = new Date(startYear, 0, (parseInt(startWeek) - 1) * 7 + 1);
            const endDate = new Date(endYear, 0, (parseInt(endWeek) - 1) * 7 + 1);
            eachWeekOfInterval({ start: startDate, end: endDate }, { weekStartsOn: 1 }).forEach(week => {
                const weekOrders = orders.filter(order => {
                    return isSameWeek(startOfDay(new Date(order.date)), startOfDay(week), { weekStartsOn: 1 })
                })
                const weekExpenses = expenses.filter(expense => {
                    return isSameWeek(startOfDay(new Date(expense.date)), startOfDay(week), { weekStartsOn: 1 })
                })
                const ordersPrice = weekOrders.reduce((total, order) => total + order.price, 0);
                const expensesPrice = weekExpenses.reduce((total, expense) => total + expense.total, 0);
                expensesPrices.push(expensesPrice)
                ordersPrices.push(ordersPrice)
                incomePrices.push(ordersPrice - expensesPrice)
            })
            break;
        case 'month':
            eachMonthOfInterval({ start: dateFilter.fromDate, end: dateFilter.toDate }).forEach(month => {
                const monthOrders = orders.filter(order => {
                    return isSameMonth(startOfDay(new Date(order.date)), startOfDay(month))
                })
                const monthExpenses = expenses.filter(expense => {
                    return isSameMonth(startOfDay(new Date(expense.date)), month)
                })
                const ordersPrice = monthOrders.reduce((total, order) => total + order.price, 0);
                const expensesPrice = monthExpenses.reduce((total, expense) => total + expense.total, 0);
                expensesPrices.push(expensesPrice)
                ordersPrices.push(ordersPrice)
                incomePrices.push(ordersPrice - expensesPrice)
            })
            break;
        case "quarter":
            eachQuarterOfInterval({ start: dateFilter.fromDate, end: endOfYear(dateFilter.toDate) }).forEach(quarter => {
                const quarterOrders = orders.filter(order => {
                    return isSameQuarter(startOfDay(new Date(order.date)), quarter)
                })
                const quarterExpenses = expenses.filter(expense => {
                    return isSameQuarter(startOfDay(new Date(expense.date)), quarter)
                })
                const ordersPrice = quarterOrders.reduce((total, order) => total + order.price, 0);
                const expensesPrice = quarterExpenses.reduce((total, expense) => total + expense.total, 0);
                expensesPrices.push(expensesPrice)
                ordersPrices.push(ordersPrice)
                incomePrices.push(ordersPrice - expensesPrice)
            })
            break;
        case "year":
            eachYearOfInterval({ start: dateFilter.fromDate, end: endOfYear(dateFilter.toDate) }).forEach(year => {
                const yearOrders = orders.filter(order => {
                    return isSameYear(startOfDay(new Date(order.date)), year)
                })
                const yearExpenses = expenses.filter(expense => {
                    return isSameYear(startOfDay(new Date(expense.date)), year)
                })
                const ordersPrice = yearOrders.reduce((total, order) => total + order.price, 0);
                const expensesPrice = yearExpenses.reduce((total, expense) => total + expense.total, 0);
                expensesPrices.push(expensesPrice)
                ordersPrices.push(ordersPrice)
                incomePrices.push(ordersPrice - expensesPrice)
            })
            break;
    }
    incomeChartObj.data.datasets[0].data = incomePrices
    incomeChartObj.data.datasets[1].data = ordersPrices
    incomeChartObj.data.datasets[2].data = expensesPrices
    incomeChartObj.update()
};

watch([ordersData, expensesData], () => {
    setIncomeChartData()
}, { deep: true })

onMounted(() => {
    const ctx = incomeChart.value.getContext('2d');
    incomeChartObj = new Chart(ctx, {
        type: 'line',
        data: {
            labels: getIncomeChartLabels(),
            datasets: [{
                label: 'Прибуток',
                data: [],
                fill: false,
                borderColor: '#36A2EB',
                tension: 0.1,
            },
            {
                label: 'Дохід',
                data: [],
                fill: false,
                borderColor: '#4BC0C0',
                tension: 0.1,
            },
            {
                label: 'Витрати',
                data: [],
                fill: false,
                borderColor: '#FF6384',
                tension: 0.1,
            },
            ]
        },
    })
    setIncomeChartData();
});
</script>

<style scoped>
/* Custom CSS to change the color of Bootstrap's btn-outline-secondary */
.btn-secondary {
    /* Change text color */
    color: black;
    border-color: #DEE2E6;
    background-color: #F8F9FA;
}

.filter-ul {
    list-style-type: none;
}

.btn-secondary:active {
    color: black;
    background-color: #DEE2E6;
    border-color: #DEE2E6;
}
</style>
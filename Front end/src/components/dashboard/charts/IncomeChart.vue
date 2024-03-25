<template>
    <div>
        <div class="row g-2 align-items-center justify-content-center">
            <div class="col-auto">
                <label for="incomeRangeSelect" class="col-form-label">Статистика прибутку за </label>
            </div>
            <div class="col-auto">
                <select v-model="incomeRangeSelect" id="incomeRangeSelect" class="form-select form-select-sm">
                    <option value="week">Тиждень</option>
                    <option value="year">Рік</option>
                </select>
            </div>
        </div>
        <canvas ref="incomeChart"></canvas>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, watchEffect } from 'vue';
import { useOrdersStore } from '../../../stores/orders';
import { useExpensesStore } from '../../../stores/expenses';
import Chart from 'chart.js/auto';

const months = ['Січень',
    'Лютий',
    'Березень',
    'Квітень',
    'Травень',
    'Червень',
    'Липень',
    'Серпень',
    'Вересень',
    'Жовтень',
    'Листопад',
    'Грудень'
]
function getCurrentWeekDates() {
    let currentDate = new Date();
    let currentDay = currentDate.getDay(); // 0 (Sunday) to 6 (Saturday)
    let mondayOffset = currentDay === 0 ? -6 : 1 - currentDay; // Adjust offset for Sunday
    let mondayDate = new Date(currentDate.setDate(currentDate.getDate() + mondayOffset));
    let dates = [];

    for (let i = 0; i < 7; i++) {
        let date = new Date(mondayDate);
        date.setDate(mondayDate.getDate() + i);
        dates.push(date.getDate());
    }

    return dates;
}

let incomeChartObj = null
const incomeChart = ref(null);
const incomeRangeSelect = ref("week")
const incomeLabels = computed(() => {
    return incomeRangeSelect.value === 'week' ? getCurrentWeekDates() : months;
});
const incomeData = computed(() => {
    const data = []
    if (incomeRangeSelect.value === 'year') {
        const orders = useOrdersStore().ordersData.filter((order) => {
            order.month = new Date(order.date).getMonth()
            return new Date(order.date).getYear() === new Date().getYear()
        })
        const expenses = useExpensesStore().expensesData.filter((expense) => {
            expense.month = new Date(expense.date).getMonth()
            return new Date(expense.date).getYear() === new Date().getYear()
        })
        for (let month = 0; month <= 11; month++) {
            let total = 0
            orders.filter((order) => order.month === month).forEach(order => {
                total += order.price
            });
            expenses.filter((expense) => expense.month === month).forEach(expense => {
                total -= expense.total
            });
            data.push(total)
        }
    } else {
        let currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);
        let currentDay = currentDate.getDay(); // 0 (Sunday) to 6 (Saturday)
        let mondayOffset = currentDay === 0 ? -6 : 1 - currentDay; // Adjust offset for Sunday
        const mondayDate = new Date(currentDate.setDate(currentDate.getDate() + mondayOffset));
        const sundayDate = new Date(mondayDate);
        sundayDate.setDate(mondayDate.getDate() + 6);
        const orders = useOrdersStore().ordersData.filter((order) => {
            const date = new Date(order.date)
            order.day = new Date(order.date).getDay() === 0 ? 6 : new Date(order.date).getDay() - 1
            return mondayDate <= new Date(date.getFullYear(), date.getMonth(), date.getDate()) && new Date(date.getFullYear(), date.getMonth(), date.getDate()) <= sundayDate;
        })
        const expenses = useExpensesStore().expensesData.filter((expense) => {
            const date = new Date(expense.date)
            expense.day = new Date(expense.date).getDay() === 0 ? 6 : new Date(expense.date).getDay() - 1
            return mondayDate <= new Date(date.getFullYear(), date.getMonth(), date.getDate()) && new Date(date.getFullYear(), date.getMonth(), date.getDate()) <= sundayDate;
        })

        for (let day = 0; day <= 6; day++) {
            let total = 0
            orders.filter((order) => order.day === day).forEach(order => {
                total += order.price
            });
            expenses.filter((expense) => expense.day === day).forEach(expense => {
                total -= expense.total
            });
            data.push(total)
        }
    }
    return data
});


onMounted(() => {
    const ctx = incomeChart.value.getContext('2d');
    incomeChartObj = new Chart(ctx, {
        type: 'line',
        data: {
            labels: incomeLabels.value,
            datasets: [{
                data: incomeData.value,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    })
});

watch(() => incomeRangeSelect.value, () => {
    incomeChartObj.data.labels = incomeLabels.value
    incomeChartObj.data.datasets[0].data = incomeData.value
    incomeChartObj.update()
}, { deep: true })
</script>
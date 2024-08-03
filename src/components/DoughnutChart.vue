<template>
    <div class="doughnut-chart-container">
        <doughnut :data="data" :options="options" />
        <div class="chart-label">
            {{ centerLabel }}
            <div>{{ centerText }}</div>
        </div>
    </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

export default {
    name: 'DoughnutChart',
    components: {
        Doughnut
    },
    props: {
        data: {
            type: Object,
            required: true
        },
        centerLabel: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                let label = tooltipItem.label || ''
                                if (label) {
                                    label += ': '
                                }
                                label += Math.round(tooltipItem.raw * 100) / 100
                                return label
                            }
                        }
                    }
                }
            }
        }
    },
    computed: {
        effectivePercentage() {
            const total = this.data.datasets[0].data.reduce((acc, val) => acc + val, 0)
            const effective = this.data.datasets[0].data[0] // assuming the first index is the effective count
            return ((effective / total) * 100).toFixed(2)
        },
        centerText() {
            return `${this.effectivePercentage}%`
        }
    }
}
</script>

<style scoped>
.doughnut-chart-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}

.chart-label {
    position: absolute;
    font-size: 1.5em;
    color: #000;
    text-align: center;
}
</style>

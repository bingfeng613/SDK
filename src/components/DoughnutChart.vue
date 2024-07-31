<template>
    <div>
        <doughnut :data="data" :options="options" />
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
        }
    },
    data() {
        return {
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    }
}
</script>

<style scoped>
canvas {
    width: 20% ;
    height: 20% ;
}
</style>

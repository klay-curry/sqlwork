<template>
  <v-chart :option="option" style="height: 400px;" autoresize />
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent, TitleComponent])

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const option = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: props.data.map(item => item.name) || [],
    axisLabel: {
      interval: 0,
      rotate: 30
    }
  },
  yAxis: {
    type: 'value',
    name: '销量'
  },
  series: [{
    name: '销量',
    data: props.data.map(item => item.sales) || [],
    type: 'bar',
    itemStyle: {
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: '#91cc75' },
          { offset: 1, color: '#5470c6' }
        ]
      }
    },
    label: {
      show: true,
      position: 'top'
    }
  }]
}))
</script>

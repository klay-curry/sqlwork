<template>
  <v-chart :option="option" style="height: 400px;" autoresize />
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, TitleComponent])

const props = defineProps({
  data: {
    type: Object,
    default: () => ({ dates: [], sales: [] })
  }
})

const option = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
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
    boundaryGap: false,
    data: props.data.dates || []
  },
  yAxis: {
    type: 'value',
    name: '销量'
  },
  series: [{
    name: '销量',
    data: props.data.sales || [],
    type: 'line',
    smooth: true,
    itemStyle: {
      color: '#5470c6'
    },
    areaStyle: {
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(84, 112, 198, 0.3)' },
          { offset: 1, color: 'rgba(84, 112, 198, 0.1)' }
        ]
      }
    }
  }]
}))
</script>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  panels: Number,
  leftPanels: Number,
  rightPanels: Number,
  cutHeight: Number,
  meters: Number,
  leftRatio: Number,
})
const left = computed(() => props.leftPanels ?? 0)
const right = computed(() => props.rightPanels ?? 0)
const bars = (n) => Array.from({ length: Math.min(n || 0, 8) }, (_, i) => i + 1)
</script>
<template>
  <div class="panel-cut-wrap">
    <div class="panel-cut">
      <div class="panel-side">
        <span class="side-label">左 {{ left }} 幅<span v-if="leftRatio != null">（{{ Math.round((leftRatio || 0) * 100) }}%）</span></span>
        <div class="panel-row">
          <div v-for="n in bars(left)" :key="'l' + n" class="panel" :style="{height: `${(cutHeight||1)*40}px`}"></div>
        </div>
      </div>
      <div class="panel-divider"></div>
      <div class="panel-side">
        <span class="side-label">右 {{ right }} 幅</span>
        <div class="panel-row">
          <div v-for="n in bars(right)" :key="'r' + n" class="panel panel-right" :style="{height: `${(cutHeight||1)*40}px`}"></div>
        </div>
      </div>
    </div>
    <p>{{ panels }} 幅（左 {{ left }} / 右 {{ right }}）× {{ cutHeight }} m = {{ meters }} m</p>
  </div>
</template>

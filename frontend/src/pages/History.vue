<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1>
<ul>
  <li v-for="r in items" :key="r.id">
    #{{ r.id }} {{ r.window_name }} {{ r.result?.meters }}m
    <template v-if="r.result && 'left_panels' in r.result">（左 {{ r.result.left_panels }} / 右 {{ r.result.right_panels }}，占比 {{ r.result.left_ratio }}）</template>
  </li>
</ul>
<p class="hint">左右幅数与占比均为落库时的分幅结果，打开后不再重切。</p>
</div></template>

<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const props = defineProps({ id: String })
const w = ref(null)
const lastRun = ref(null)
onMounted(async () => {
  w.value = await getJSON(`/api/windows/${props.id}`)
  const runs = (await getJSON(`/api/runs?window_id=${props.id}&limit=1`)).items
  lastRun.value = runs.length ? runs[0] : null
})
</script>
<template><div class="page" v-if="w"><h1>{{ w.name }}</h1>
<p v-if="w.data_quality==='dirty'" class="bad">{{ w.note }}</p>
<p>宽 {{ w.width }} 高 {{ w.height }} 褶倍 {{ w.fullness }}</p>
<section v-if="lastRun" class="last-run">
  <h2>当次分幅 <small>#{{ lastRun.id }}</small></h2>
  <PanelCut
    :panels="lastRun.result.panels"
    :left-panels="lastRun.result.left_panels"
    :right-panels="lastRun.result.right_panels"
    :cut-height="lastRun.result.cut_height"
    :meters="lastRun.result.meters"
    :left-ratio="lastRun.result.left_ratio"
  />
</section>
<p v-else>暂无落库记录</p>
</div></template>

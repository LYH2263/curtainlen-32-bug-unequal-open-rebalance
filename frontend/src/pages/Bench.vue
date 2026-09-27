<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null)
const ratio = ref(0.5); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
})
async function go(save){
  err.value = ''
  try {
    const r = Number(ratio.value)
    out.value = save
      ? await postJSON('/api/estimate',{window_id:wid.value,fabric_id:fid.value,save:true,left_ratio:r})
      : await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}&left_ratio=${r}`)
  } catch (e) {
    out.value = null
    err.value = '试算失败：' + e.message
  }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label class="ratio">左侧占比
  <input type="number" v-model.number="ratio" min="0" max="1" step="0.05" />
  <input type="range" v-model.number="ratio" min="0" max="1" step="0.05" />
</label>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<PanelCut v-if="out" :panels="out.panels" :left-panels="out.left_panels" :right-panels="out.right_panels" :cut-height="out.cut_height" :meters="out.meters" :left-ratio="out.left_ratio" />
</div></template>

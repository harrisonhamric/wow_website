<template>
  <div class="container">
    <h2>Edit {{ model.name }}</h2>
    <form @submit.prevent="onSubmit">
      <label>
        Level:
        <input type="number" v-model.number="model.level" min="1" required />
      </label><br/>
      <label>
        Professions (comma‑sep):
        <input v-model="profText" placeholder="Mining, Herbalism" />
      </label><br/>
      <button type="submit">Save</button>
      <router-link to="/view">Cancel</router-link>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import type { Character } from '../services/characterService';
import { getCharacter, updateCharacter } from '../services/characterService';

const router = useRouter();
const route  = useRoute();
const id      = Number(route.params.id);

const model   = ref<Character>({
  id: undefined, name: '', class: '', spec: '', level: 1, professions: []
});
const profText = ref('');

onMounted(async () => {
  try {
    const char = await getCharacter(id);
    model.value = char;
    profText.value = char.professions.join(', ');
  } catch (err) {
    console.error(err);
    alert('Failed to load character');
    router.push('/view');
  }
});

async function onSubmit() {
  const profsArray = profText.value
    .split(',')
    .map(p => p.trim())
    .filter(p => p);

  try {
    await updateCharacter(id, {
      level: model.value.level,
      professions: profsArray
    });
    alert('Character updated!');
    router.push('/view');
  } catch (err) {
    console.error(err);
    alert('Failed to update character');
  }
}
</script>

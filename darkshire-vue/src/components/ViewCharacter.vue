<!-- <template>
  <div class="container">
    <h2>All Characters</h2>
    <div v-if="list.length">
      <div v-for="c in list" :key="c.id" class="char-card">
        <h3>{{ c.name }} (Lvl {{ c.level }} {{ c.class }})</h3>
        <p>Professions: {{ c.professions.join(', ') }}</p>
        <img v-if="c.photo_url"
             :src="c.photo_url"
             alt="Character photo"
             style="max-width:200px; margin-top:0.5em;" />
        <button @click="$router.push(`/edit/${c.id}`)">Edit</button>
      </div>
    </div>
    <p v-else>No characters yet.</p>
  </div>
</template> -->

<template>
  <div class="container">
    <h2 class="page-title">All Characters</h2>
    <div class="char-list" v-if="list.length">
      <div v-for="c in list" :key="c.id" class="char-item">
        <div class="char-name-box">
          <h3>{{ c.name }}</h3>
          <img v-if="c.photo_url" :src="c.photo_url" alt="Character photo"/>
        </div>
        <p>Class: {{ c.class }}</p>
        <p>Level: {{ c.level }}</p>
        <p>Spec: {{ c.spec }}</p>
        <p>Professions: {{ c.professions.join(', ') }}</p>
        <button class="edit-button" @click="$router.push(`/edit/${c.id}`)">Edit</button>
      </div>
    </div>
    <p v-else>No characters yet.</p>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Character } from '../services/characterService';
import { listCharacters } from '../services/characterService';

const list = ref<Character[]>([]);
onMounted(async () => {
  list.value = await listCharacters();
});
</script>
<template>
  <div class="container">
    <h2 class="page-title">Add Character</h2>
    <form @submit.prevent="onSubmit">
      <div class="form-row">
        <label>Name:</label>
        <div><input v-model="model.name" required /></div>
      </div>
      <div class="form-row">
        <label>Class:</label>
        <div>
          <select v-model="model.class" required>
            <option disabled value="">Select a class</option>
            <option v-for="c in wowClasses" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <label>Spec:</label>
        <div><input v-model="model.spec" required /></div>
      </div>
      <div class="form-row">
        <label>Level:</label>
        <div><input type="number" v-model.number="model.level" min="1" required /></div>
      </div>
      <div class="form-row">
        <label>Professions:</label>
        <div><input v-model="profText" placeholder="Mining, Herbalism" /></div>
      </div>
      <div class="form-row">
        <label>Photo:</label>
        <div><input type="file" @change="onFileChange" accept="image/*" /></div>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<!-- <template>
  <div class="container">
    <h2>Add Character</h2>
    <form @submit.prevent="onSubmit">
      <label>
        Name:
        <input v-model="model.name" required /> </label
      ><br />
      <label>
        Class:
        <!-- <input v-model="model.class" required />  -->
         <!--
        <select v-model="model.class" required>
          <option disabled value="">Select a class</option>
          <option v-for="c in wowClasses" :key="c" :value="c">{{ c }}</option>
        </select>
      </label>
      <br />
      <label>
        Spec:
        <input v-model="model.spec" placeholder="e.g., Fire, Protection" required />
      </label>
      <br />
      <label>
        Level:
        <input type="number" v-model.number="model.level" min="1" /> 
      </label><br />
      <label>
        Professions (comma‑sep):
        <input v-model="profText" placeholder="Mining, Herbalism" /> </label
      ><br />
      <label>
        Photo:
        <input type="file" @change="onFileChange" accept="image/*" />
      </label><br/>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>
 -->
<script setup lang="ts">
import { ref } from 'vue';
import type { Character } from '../services/characterService';
import { uploadCharacter } from '../services/characterService';

// WoW Classes List
const wowClasses = [
  "Death Knight", 
  "Demon Hunter", 
  "Druid",
  "Evoker",
  "Hunter",
  "Mage",
  "Monk",
  "Paladin",
  "Priest",
  "Rogue",
  "Shaman",
  "Warlock",
  "Warrior"]

const model    = ref<Character> ({ 
  name:'', 
  class:'', 
  spec: '', 
  level:1, 
  professions:[] 
});
const profText = ref('');
const photo    = ref<File|null>(null);

function onFileChange(e: Event) {
  const f = (e.target as HTMLInputElement).files;
  if (f && f[0]) photo.value = f[0];
}

async function onSubmit() {
  // build formData
  const fd = new FormData();
  fd.append('name', model.value.name);
  fd.append('class', model.value.class);
  fd.append('spec', model.value.spec);
  fd.append('level', model.value.level.toString());
  fd.append('professions',
            profText.value.split(',')
                         .map(p=>p.trim())
                         .filter(p=>p)
                         .join(','));
  if (photo.value) fd.append('photo', photo.value);

  try {
    await uploadCharacter(fd);
    alert('Character added!');
    // reset
    model.value    = { name:'', class:'',  spec: '', level:1, professions:[] };
    profText.value = '';
    photo.value    = null;
  } catch (err) {
    console.error(err);
    alert('Error uploading character');
  }
}
</script>

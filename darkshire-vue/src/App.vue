<script setup lang="ts"></script>

<template>
  <nav class="top-nav-bar">
    <router-link to="/" class="nav-title">The Darkshire Zone</router-link>
  </nav>
  <nav class="nav-bar">
    <router-link to="/view">View Characters</router-link>
    <router-link to="/add">Add Characters</router-link>
  </nav>
  <router-view />
</template>

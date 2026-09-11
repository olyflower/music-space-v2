<script setup lang="ts">
import { RouterView } from "vue-router";
import AppHeader from "@/components/AppHeader.vue";
</script>

<template>
	<AppHeader />

	<main class="pb-20 sm:pb-0">
		<RouterView />
	</main>
</template>

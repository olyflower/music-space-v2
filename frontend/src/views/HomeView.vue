<script setup lang="ts">
import { ref } from "vue";

interface Track {
	spotify_id: string;
	title: string;
	artist: string;
	album: string;
	duration_ms: number;
	cover_url: string | null;
	spotify_url: string;
}

const query = ref("");
const tracks = ref<Track[]>([]);
const loading = ref(false);
const error = ref("");

async function searchTracks() {
	if (!query.value.trim()) return;

	loading.value = true;
	error.value = "";

	try {
		const response = await fetch(
			`http://localhost:8000/api/search/?q=${encodeURIComponent(query.value)}`,
		);
		if (!response.ok) throw new Error("Search failed");
		const data = await response.json();
		tracks.value = data.results;
	} catch (e) {
		error.value = "Something went wrong. Try again.";
	} finally {
		loading.value = false;
	}
}
</script>

<template>
	<main>
		<h1>Music Search</h1>

		<form @submit.prevent="searchTracks">
			<input
				v-model="query"
				type="text"
				placeholder="Search for a track or artist..."
			/>
			<button type="submit">Search</button>
		</form>

		<p v-if="loading">Loading...</p>
		<p v-if="error">{{ error }}</p>

		<ul v-if="tracks.length">
			<li v-for="track in tracks" :key="track.spotify_id">
				<img
					v-if="track.cover_url"
					:src="track.cover_url"
					:alt="track.title"
					width="60"
				/>
				<div>
					<strong>{{ track.title }}</strong> — {{ track.artist }}
					<br />
					<a :href="track.spotify_url" target="_blank"
						>Listen on Spotify</a
					>
				</div>
			</li>
		</ul>
	</main>
</template>

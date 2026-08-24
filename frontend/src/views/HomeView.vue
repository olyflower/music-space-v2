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
	<main class="max-w-2xl mx-auto px-4 py-8">
		<h1 class="text-3xl font-bold mb-6 text-gray-900">Music Search</h1>

		<form @submit.prevent="searchTracks" class="flex gap-2 mb-8">
			<input
				v-model="query"
				type="text"
				placeholder="Search for a track or artist..."
				class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
			/>
			<button
				type="submit"
				class="px-5 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
			>
				Search
			</button>
		</form>

		<p v-if="loading" class="text-gray-500">Loading...</p>
		<p v-if="error" class="text-red-500">{{ error }}</p>

		<ul v-if="tracks.length" class="space-y-3">
			<li
				v-for="track in tracks"
				:key="track.spotify_id"
				class="flex items-center gap-4 py-3 border-b border-gray-100"
			>
				<img
					v-if="track.cover_url"
					:src="track.cover_url"
					:alt="track.title"
					class="w-14 h-14 rounded-md shrink-0"
				/>
				<div>
					<p class="font-semibold text-gray-900">
						{{ track.title }}
						<span class="text-gray-500 font-normal"
							>— {{ track.artist }}</span
						>
					</p>
					<a
						:href="track.spotify_url"
						target="_blank"
						class="text-sm text-green-600 hover:underline"
					>
						Listen on Spotify
					</a>
				</div>
			</li>
		</ul>
	</main>
</template>

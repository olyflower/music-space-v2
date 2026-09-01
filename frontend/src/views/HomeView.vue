<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { useFavoritesStore } from "@/stores/favorites";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

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

const auth = useAuthStore();
const favorites = useFavoritesStore();

async function searchTracks() {
	if (!query.value.trim()) return;

	loading.value = true;
	error.value = "";

	try {
		const { data } = await axios.get(`${API_BASE}/search/`, {
			params: { q: query.value },
		});
		tracks.value = data.results;
	} catch (e) {
		error.value = "Something went wrong. Try again.";
	} finally {
		loading.value = false;
	}
}

async function toggleFavorite(track: Track) {
	if (!auth.userEmail) {
		alert("Please sign in to save favorites");
		return;
	}

	try {
		if (favorites.favoriteIds.has(track.spotify_id)) {
			await favorites.removeFavorite(track.spotify_id);
		} else {
			await favorites.addFavorite(track);
		}
	} catch (e) {
		alert("Something went wrong");
	}
}
</script>

<template>
	<div class="bg-surface border-b border-border">
		<div class="max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
			<h1
				class="font-display font-bold text-3xl sm:text-4xl text-ink mb-2"
			>
				Find your next favorite
			</h1>
			<p class="text-sm sm:text-base text-muted mb-6">
				Search millions of tracks, save what moves you.
			</p>

			<form @submit.prevent="searchTracks" class="flex gap-2 max-w-xl">
				<input
					v-model="query"
					type="text"
					name="music-search"
					autocomplete="on"
					placeholder="Search for a track or artist..."
					class="flex-1 px-4 py-3 bg-white border border-border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
				/>
				<button
					type="submit"
					class="px-6 py-3 bg-forest text-white text-sm font-medium rounded-xl hover:bg-forest/90 transition-colors"
				>
					Search
				</button>
			</form>
		</div>
	</div>

	<main class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
		<p v-if="loading" class="text-sm text-muted">Loading...</p>
		<p v-if="error" class="text-sm text-coral">{{ error }}</p>

		<ul v-if="tracks.length" class="space-y-1">
			<li
				v-for="track in tracks"
				:key="track.spotify_id"
				class="flex items-center gap-4 p-3 rounded-xl hover:bg-surface transition-colors"
			>
				<img
					v-if="track.cover_url"
					:src="track.cover_url"
					:alt="track.title"
					class="w-12 h-12 rounded-lg shrink-0"
				/>
				<div class="flex-1 min-w-0">
					<p class="text-sm font-semibold text-ink truncate">
						{{ track.title }}
						<span class="text-muted font-normal"
							>— {{ track.artist }}</span
						>
					</p>
					<p class="text-xs text-muted mt-0.5">{{ track.album }}</p>
				</div>
				<a
					:href="track.spotify_url"
					target="_blank"
					class="text-xs text-forest hover:underline shrink-0"
				>
					Listen
				</a>
				<button
					@click="toggleFavorite(track)"
					class="text-lg shrink-0"
					:class="
						favorites.favoriteIds.has(track.spotify_id)
							? 'text-coral'
							: 'text-border hover:text-muted'
					"
				>
					♥
				</button>
			</li>
		</ul>

		<div
			v-if="!loading && !tracks.length && !error"
			class="text-center py-16"
		>
			<p class="text-sm text-muted">Search above to discover tracks.</p>
		</div>
	</main>
</template>

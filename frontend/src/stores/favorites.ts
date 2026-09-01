import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from "axios";

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

export const useFavoritesStore = defineStore("favorites", () => {
	const tracks = ref<Track[]>([]);
	const loaded = ref(false);

	const favoriteIds = computed(
		() => new Set(tracks.value.map((t) => t.spotify_id)),
	);

	async function loadFavorites(force = false) {
		if (loaded.value && !force) return;

		const { data } = await axios.get(`${API_BASE}/favorites/`, {
			withCredentials: true,
		});
		tracks.value = data.results;
		loaded.value = true;
	}

	async function addFavorite(track: Track) {
		tracks.value.push(track);
		try {
			await axios.post(
				`${API_BASE}/favorites/add/`,
				{ track },
				{ withCredentials: true },
			);
		} catch (e) {
			tracks.value = tracks.value.filter(
				(t) => t.spotify_id !== track.spotify_id,
			);
			throw e;
		}
	}

	async function removeFavorite(spotifyId: string) {
		const backup = tracks.value.find((t) => t.spotify_id === spotifyId);
		tracks.value = tracks.value.filter((t) => t.spotify_id !== spotifyId);

		try {
			await axios.delete(`${API_BASE}/favorites/${spotifyId}/`, {
				withCredentials: true,
			});
		} catch (e) {
			if (backup) tracks.value.push(backup);
			throw e;
		}
	}

	function reset() {
		tracks.value = [];
		loaded.value = false;
	}

	return {
		tracks,
		loaded,
		favoriteIds,
		loadFavorites,
		addFavorite,
		removeFavorite,
		reset,
	};
});

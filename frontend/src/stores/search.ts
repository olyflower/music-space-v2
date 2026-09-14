import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { toast } from "vue3-toastify";
import type { Track } from "@/types/track";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const useSearchStore = defineStore("search", () => {
	const query = ref("");
	const tracks = ref<Track[]>([]);
	const loading = ref(false);

	async function searchTracks() {
		const searchQuery = query.value.trim();

		if (!searchQuery || loading.value) return;

		loading.value = true;
		tracks.value = [];

		try {
			const { data } = await axios.get(`${API_BASE}/search/`, {
				params: {
					q: searchQuery,
				},
			});

			tracks.value = data.results ?? [];
		} catch {
			toast.error("Something went wrong. Try again.");
		} finally {
			loading.value = false;
		}
	}

	function resetSearch() {
	query.value = "";
	tracks.value = [];
	loading.value = false;
}

	return {
		query,
		tracks,
		loading,
		searchTracks,
		resetSearch,
	};
});

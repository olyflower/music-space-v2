import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { useSearchStore } from "@/stores/search";
import { useFavoritesStore } from "@/stores/favorites";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const useAuthStore = defineStore("auth", () => {
	const userEmail = ref<string | null>(null);
	const userName = ref<string | null>(null);
	const isLoading = ref(true);

	async function checkAuth() {
		isLoading.value = true;
		try {
			const { data } = await axios.get(`${API_BASE}/auth/current-user/`, {
				withCredentials: true,
			});
			userEmail.value = data.email;
			userName.value = data.name;
		} catch {
			userEmail.value = null;
			userName.value = null;
		} finally {
			isLoading.value = false;
		}
	}

	async function loginWithGoogle(googleToken: string) {
		const { data } = await axios.post(
			`${API_BASE}/auth/google/`,
			{ token: googleToken },
			{ withCredentials: true },
		);
		userEmail.value = data.user.email;
		userName.value = data.user.name;
	}

	async function logout() {
		const searchStore = useSearchStore();
		const favoritesStore = useFavoritesStore();

		searchStore.resetSearch();
		favoritesStore.reset();

		userEmail.value = null;
		userName.value = null;

		await axios.post(
			`${API_BASE}/auth/logout/`,
			{},
			{ withCredentials: true },
		);
	}

	return {
		userEmail,
		userName,
		isLoading,
		checkAuth,
		loginWithGoogle,
		logout,
	};
});

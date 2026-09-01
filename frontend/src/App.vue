<script setup lang="ts">
import { RouterView, RouterLink } from "vue-router";
import { GoogleLogin } from "vue3-google-login";
import { useAuthStore } from "@/stores/auth";
import { useFavoritesStore } from "./stores/favorites";
import { onMounted, watch, computed } from "vue";

const auth = useAuthStore();
const favorites = useFavoritesStore();

const initials = computed(() => {
	const name = auth.userName || auth.userEmail || "";
	return name.slice(0, 2).toUpperCase();
});

onMounted(() => {
	auth.checkAuth();
});

watch(
	() => auth.userEmail,
	(email) => {
		if (email) {
			favorites.loadFavorites(true);
		} else {
			favorites.reset();
		}
	},
	{ immediate: true },
);

async function handleGoogleLogin(response: any) {
	await auth.loginWithGoogle(response.credential);
}
</script>

<template>
	<header class="border-b border-border px-4 sm:px-6 py-4">
		<div class="max-w-2xl mx-auto flex items-center justify-between gap-4">
			<div class="flex items-center gap-4 sm:gap-6 min-w-0">
				<span
					class="font-display font-semibold text-base sm:text-lg text-ink shrink-0"
					>Music Space</span
				>
				<nav class="flex items-center gap-4 sm:gap-6">
					<RouterLink
						to="/"
						class="text-sm font-medium text-ink pb-1"
						:class="
							$route.path === '/'
								? 'border-b-2 border-forest'
								: 'text-muted'
						"
					>
						Search
					</RouterLink>
					<RouterLink
						to="/favorites"
						class="text-sm font-medium text-ink pb-1"
						:class="
							$route.path === '/favorites'
								? 'border-b-2 border-forest'
								: 'text-muted'
						"
					>
						Favorites
					</RouterLink>
				</nav>
			</div>

			<div v-if="auth.isLoading" class="text-sm text-muted shrink-0">
				Loading...
			</div>

			<div
				v-else-if="auth.userEmail"
				class="flex items-center gap-2 sm:gap-3 shrink-0"
			>
				<div
					class="w-7 h-7 rounded-full bg-forest text-white text-xs font-semibold flex items-center justify-center shrink-0"
				>
					{{ initials }}
				</div>
				<span class="hidden sm:inline text-sm text-muted">{{
					auth.userName || auth.userEmail
				}}</span>
				<button
					@click="auth.logout()"
					class="text-sm text-muted hover:text-ink"
				>
					Log out
				</button>
			</div>

			<GoogleLogin v-else :callback="handleGoogleLogin" />
		</div>
	</header>

	<RouterView />
</template>

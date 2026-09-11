<script setup lang="ts">
import { useRoute, RouterLink } from "vue-router";
import { GoogleLogin } from "vue3-google-login";
import { useAuthStore } from "@/stores/auth";
import { useFavoritesStore } from "@/stores/favorites";
import { onMounted, watch, computed, ref } from "vue";

interface GoogleLoginResponse {
	credential: string;
}

const route = useRoute();
const auth = useAuthStore();
const favorites = useFavoritesStore();

const isUserMenuOpen = ref(false);

function toggleUserMenu() {
	isUserMenuOpen.value = !isUserMenuOpen.value;
}

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

async function handleGoogleLogin(response: GoogleLoginResponse) {
	await auth.loginWithGoogle(response.credential);
}
</script>

<template>
	<header
		class="sticky top-0 z-50 border-b border-border bg-white/90 backdrop-blur-xl"
	>
		<div
			class="mx-auto flex h-18 max-w-6xl items-center justify-between px-5 sm:px-8 lg:px-10"
		>
			<!-- Logo -->
			<RouterLink to="/" class="group flex items-center gap-2">
				<span
					class="flex h-10 w-10 items-center justify-center rounded-xl bg-linear-to-br from-accent to-purple text-base font-semibold text-white transition duration-200 group-hover:scale-105"
				>
					♫
				</span>

				<span class="text-base font-semibold text-ink">
					Music Space
				</span>
			</RouterLink>

			<!-- Desktop navigation -->
			<nav
				class="absolute left-1/2 hidden -translate-x-1/2 items-center gap-1 rounded-full bg-surface p-1 sm:flex"
			>
				<RouterLink
					to="/"
					class="rounded-full px-5 py-2 text-sm font-medium transition"
					:class="
						route.path === '/'
							? 'bg-white text-accent shadow-sm'
							: 'text-muted hover:text-ink'
					"
				>
					Search
				</RouterLink>

				<RouterLink
					to="/favorites"
					class="rounded-full px-5 py-2 text-sm font-medium transition"
					:class="
						route.path === '/favorites'
							? 'bg-white text-accent shadow-sm'
							: 'text-muted hover:text-ink'
					"
				>
					Favorites
				</RouterLink>
			</nav>

			<!-- User -->
			<div class="flex items-center gap-3">
				<div v-if="auth.isLoading" class="text-sm text-muted">
					Loading...
				</div>

				<div
					v-else-if="auth.userEmail"
					class="relative flex items-center gap-3"
				>
					<!-- Desktop user -->
					<div class="hidden items-center gap-3 md:flex">
						<div
							class="flex h-9 w-9 items-center justify-center rounded-full bg-linear-to-br from-accent to-purple text-xs font-bold text-white"
						>
							{{ initials }}
						</div>

						<div>
							<p
								class="max-w-37.5 truncate text-sm font-semibold text-ink"
							>
								{{ auth.userName || auth.userEmail }}
							</p>

							<button
								@click="auth.logout()"
								class="mt-0.5 text-xs text-muted transition-colors hover:text-accent"
							>
								Log out
							</button>
						</div>
					</div>

					<!-- Mobile user -->
					<div class="relative md:hidden">
						<button
							type="button"
							aria-label="Open user menu"
							:aria-expanded="isUserMenuOpen"
							class="flex h-10 w-10 items-center justify-center rounded-full bg-linear-to-br from-accent to-purple text-xs font-bold text-white transition duration-200 hover:scale-105"
							@click="toggleUserMenu"
						>
							{{ initials }}
						</button>

						<div
							v-if="isUserMenuOpen"
							class="absolute right-0 top-12 w-36 rounded-xl border border-border bg-white p-1.5 shadow-lg"
						>
							<p class="truncate px-3 py-2 text-xs text-muted">
								{{ auth.userName || auth.userEmail }}
							</p>

							<button
								type="button"
								class="w-full rounded-lg px-3 py-2 text-left text-sm font-medium text-ink transition-colors hover:bg-surface hover:text-accent"
								@click="auth.logout()"
							>
								Log out
							</button>
						</div>
					</div>
				</div>

				<div v-else>
					<!-- Desktop -->
					<div class="hidden sm:block">
						<GoogleLogin
							:callback="handleGoogleLogin"
							:button-config="{
								type: 'standard',
								theme: 'outline',
								size: 'medium',
								shape: 'pill',
								text: 'signin_with',
							}"
						/>
					</div>

					<!-- Mobile -->
					<div class="sm:hidden">
						<GoogleLogin
							:callback="handleGoogleLogin"
							:button-config="{
								type: 'standard',
								theme: 'outline',
								size: 'small',
								shape: 'pill',
								text: 'signin',
							}"
						/>
					</div>
				</div>
			</div>
		</div>
	</header>

	<!-- Mobile navigation -->
	<nav
		class="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-white/95 backdrop-blur-xl sm:hidden"
	>
		<div class="mx-auto grid max-w-md grid-cols-2">
			<RouterLink
				to="/"
				class="flex flex-col items-center gap-1 py-3 text-xs transition-colors"
				:class="
					route.path === '/'
						? 'font-semibold text-accent'
						: 'text-muted'
				"
			>
				<span class="text-lg">⌕</span>
				Search
			</RouterLink>

			<RouterLink
				to="/favorites"
				class="flex flex-col items-center gap-1 py-3 text-xs transition-colors"
				:class="
					route.path === '/favorites'
						? 'font-semibold text-accent'
						: 'text-muted'
				"
			>
				<span class="text-lg">♥</span>
				Favorites
			</RouterLink>
		</div>
	</nav>
</template>

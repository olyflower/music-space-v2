<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useFavoritesStore } from "@/stores/favorites";
import { useSearchStore } from "@/stores/search";
import HeroDecorations from "@/components/HeroDecorations.vue";
import type { Track } from "@/types/track";
import { toast } from "vue3-toastify";
import { features } from "@/data/home";

const auth = useAuthStore();
const search = useSearchStore();
const favorites = useFavoritesStore();

async function toggleFavorite(track: Track) {
	if (!auth.userEmail) {
		toast.error("Please sign in to save favorites");
		return;
	}

	try {
		const isFavorite = favorites.favoriteIds.has(track.spotify_id);

		if (isFavorite) {
			await favorites.removeFavorite(track.spotify_id);
			toast.success("Removed from favorites");
		} else {
			await favorites.addFavorite(track);
			toast.success("Added to favorites");
		}
	} catch {
		toast.error("Something went wrong");
	}
}
</script>

<template>
	<main class="min-h-screen overflow-hidden bg-cream">
		<!-- HERO -->
		<section
			class="relative isolate flex min-h-[calc(100vh-73px)] items-center overflow-hidden px-5 py-16 sm:px-8 lg:px-12"
		>
			<HeroDecorations />

			<div class="relative z-10 mx-auto w-full max-w-4xl text-center">
				<p
					class="text-[11px] font-bold uppercase tracking-[0.3em] text-accent"
				>
					MUSIC DISCOVERY
				</p>

				<h1
					class="mx-auto mt-6 max-w-4xl text-5xl font-bold leading-[0.98] tracking-[-0.055em] sm:text-6xl md:text-7xl lg:text-[78px]"
				>
					Discover music
					<br />
					<span
						class="bg-linear-to-r from-accent to-purple bg-clip-text text-transparent"
					>
						you'll actually love
					</span>
				</h1>

				<p
					class="mx-auto mt-7 max-w-2xl text-sm leading-6 text-muted sm:text-base sm:leading-7"
				>
					Search artists, tracks and albums. Save the music you want
					to come back to
				</p>

				<!-- SEARCH -->
				<form
					@submit.prevent="search.searchTracks"
					class="mx-auto mt-9 flex w-full max-w-2xl items-center rounded-2xl border border-border bg-white p-1.5 transition focus-within:border-accent/50"
				>
					<svg
						class="ml-4 h-5 w-5 shrink-0 text-muted"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<circle cx="11" cy="11" r="7" />
						<path d="m20 20-4-4" />
					</svg>

					<input
						v-model="search.query"
						type="text"
						name="music-search"
						autocomplete="off"
						placeholder="Search for a track or artist..."
						class="min-w-0 flex-1 bg-transparent px-3 py-4 text-sm outline-none placeholder:text-muted"
					/>

					<button
						type="submit"
						:disabled="search.loading || !search.query.trim()"
						class="shrink-0 rounded-xl bg-ink px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-accent disabled:cursor-not-allowed disabled:opacity-60"
					>
						{{ search.loading ? "Searching..." : "Search" }}
					</button>
				</form>

				<!-- FEATURES -->
				<div
					class="mx-auto mt-16 grid max-w-3xl grid-cols-1 gap-10 sm:grid-cols-3 sm:gap-6"
				>
					<div v-for="feature in features" :key="feature.title">
						<div
							class="mx-auto flex h-14 w-14 items-center justify-center rounded-full text-2xl"
							:class="[feature.background, feature.color]"
						>
							{{ feature.icon }}
						</div>

						<h3 class="mt-4 text-sm font-bold">
							{{ feature.title }}
						</h3>

						<p
							class="mx-auto mt-2 max-w-45 text-xs leading-5 text-muted sm:text-sm sm:leading-6"
						>
							{{ feature.description }}
						</p>
					</div>
				</div>
			</div>
		</section>

		<!-- RESULTS -->
		<section class="mx-auto max-w-5xl px-5 pb-20 sm:px-8 lg:px-12">
			<p
				v-if="search.loading"
				class="py-8 text-center text-sm text-muted"
			>
				Searching for music...
			</p>

			<!-- EMPTY STATE -->
			<div
				v-if="!search.loading && !search.tracks.length"
				class="pb-16 pt-4 text-center"
			>
				<h2 class="text-lg font-semibold">
					What are you listening to?
				</h2>

				<p class="mx-auto mt-2 max-w-sm text-sm leading-6 text-muted">
					Search for an artist, song or album to start discovering
					music
				</p>
			</div>

			<!-- TRACKS -->
			<div v-if="search.tracks.length">
				<div class="mb-6">
					<p
						class="text-[11px] font-bold uppercase tracking-[0.25em] text-accent"
					>
						SEARCH RESULTS
					</p>

					<h2 class="mt-2 text-2xl font-bold tracking-tight">
						Results for "{{ search.query }}"
					</h2>
				</div>

				<ul
					class="overflow-hidden rounded-2xl border border-border bg-white shadow-sm"
				>
					<li
						v-for="track in search.tracks"
						:key="track.spotify_id"
						class="group flex items-center gap-4 border-b border-border p-3 last:border-b-0 sm:p-4"
					>
						<!-- Cover -->
						<div
							class="h-16 w-16 shrink-0 overflow-hidden rounded-xl bg-surface sm:h-20 sm:w-20"
						>
							<img
								v-if="track.cover_url"
								:src="track.cover_url"
								:alt="track.title"
								class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
							/>

							<div
								v-else
								class="flex h-full w-full items-center justify-center text-xl text-muted"
							>
								♫
							</div>
						</div>

						<!-- Track info -->
						<div class="min-w-0 flex-1">
							<p
								class="truncate text-sm font-semibold sm:text-base"
							>
								{{ track.title }}
							</p>

							<p class="mt-0.5 truncate text-sm text-muted">
								{{ track.artist }}
							</p>

							<p class="mt-1 truncate text-xs text-muted">
								{{ track.album }}
							</p>
						</div>

						<!-- Listen -->
						<a
							:href="track.spotify_url"
							target="_blank"
							rel="noopener noreferrer"
							class="hidden shrink-0 rounded-lg px-3 py-2 text-xs font-semibold text-accent transition hover:bg-accent/5 sm:block"
						>
							Listen ↗
						</a>

						<!-- Favorite -->
						<button
							type="button"
							aria-label="Toggle favorite"
							class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full transition"
							:class="
								favorites.favoriteIds.has(track.spotify_id)
									? 'bg-accent/10 text-accent'
									: 'text-muted hover:bg-accent/5 hover:text-accent'
							"
							@click="toggleFavorite(track)"
						>
							<svg
								class="h-5 w-5"
								viewBox="0 0 24 24"
								fill="currentColor"
							>
								<path
									d="M12 21s-7-4.35-9.5-8.28C.5 8.82 2.42 5 6.5 5c2.04 0 3.48 1.13 4.5 2.4C12.02 6.13 13.46 5 15.5 5 19.58 5 21.5 8.82 21.5 12.72 19 16.65 12 21 12 21z"
								/>
							</svg>
						</button>
					</li>
				</ul>
			</div>
		</section>
	</main>
</template>

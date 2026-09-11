<script setup lang="ts">
import { h } from "vue";
import { toast } from "vue3-toastify";
import { useFavoritesStore } from "@/stores/favorites";

const favorites = useFavoritesStore();

interface Track {
	spotify_id: string;
	title: string;
	artist: string;
	album: string;
	duration_ms: number;
	cover_url: string | null;
	spotify_url: string;
}

async function removeFavorite(track: Track) {
	try {
		await favorites.removeFavorite(track.spotify_id);
	} catch {
		toast.error("Failed to remove track");
		return;
	}

	toast(
		() =>
			h("div", { class: "flex items-center gap-3" }, [
				h("span", `Removed "${track.title}"`),
				h(
					"button",
					{
						class: "underline font-semibold",
						onClick: async () => {
							try {
								await favorites.addFavorite(track);
								toast.success("Restored!");
							} catch {
								toast.error("Failed to restore");
							}
						},
					},
					"Undo",
				),
			]),
		{ autoClose: 4000 },
	);
}
</script>

<template>
	<div class="min-h-[calc(100vh-73px)]">
		<!-- Header -->
		<section class="px-4 sm:px-6 pt-12 sm:pt-20 pb-10">
			<div class="max-w-5xl mx-auto">
				<p
					class="text-xs font-semibold uppercase tracking-[0.2em] text-forest mb-4"
				>
					Your collection
				</p>

				<h1
					class="font-display font-bold text-4xl sm:text-5xl lg:text-6xl tracking-tight text-ink leading-[1.05]"
				>
					Your
					<span class="text-forest">favorites.</span>
				</h1>

				<p
					class="mt-5 text-base sm:text-lg text-muted leading-relaxed"
				>
					Tracks you've saved for later.
				</p>
			</div>
		</section>

		<!-- Content -->
		<main class="px-4 sm:px-6 pb-16">
			<div class="max-w-5xl mx-auto">
				<!-- Loading -->
				<div
					v-if="!favorites.loaded"
					class="flex items-center justify-center py-20"
				>
					<p class="text-sm text-muted">
						Loading your favorites...
					</p>
				</div>

				<!-- Empty -->
				<div
					v-else-if="!favorites.tracks.length"
					class="py-20 sm:py-28 text-center"
				>
					<div
						class="w-16 h-16 mx-auto mb-5 rounded-2xl bg-surface flex items-center justify-center text-2xl text-forest"
					>
						♥
					</div>

					<h2 class="text-lg font-semibold text-ink">
						No favorites yet
					</h2>

					<p
						class="mt-2 text-sm text-muted max-w-sm mx-auto"
					>
						Go back to Search and save the tracks you love.
					</p>
				</div>

				<!-- Favorites -->
				<div v-else>
					<div class="flex items-center justify-between mb-5">
						<div>
							<h2 class="text-lg font-semibold text-ink">
								Saved tracks
							</h2>

							<p class="text-sm text-muted mt-1">
								{{ favorites.tracks.length }}
								{{
									favorites.tracks.length === 1
										? "track"
										: "tracks"
								}}
							</p>
						</div>
					</div>

					<ul
						class="grid grid-cols-1 md:grid-cols-2 gap-3"
					>
						<li
							v-for="track in favorites.tracks"
							:key="track.spotify_id"
							class="group flex items-center gap-4 p-3 sm:p-4 bg-white border border-border rounded-2xl hover:border-forest/30 hover:shadow-sm transition"
						>
							<!-- Cover -->
							<div
								class="w-14 h-14 sm:w-16 sm:h-16 rounded-xl overflow-hidden bg-surface shrink-0"
							>
								<img
									v-if="track.cover_url"
									:src="track.cover_url"
									:alt="track.title"
									class="w-full h-full object-cover"
								/>

								<div
									v-else
									class="w-full h-full flex items-center justify-center text-muted text-lg"
								>
									♫
								</div>
							</div>

							<!-- Track info -->
							<div class="flex-1 min-w-0">
								<p
									class="text-sm font-semibold text-ink truncate"
								>
									{{ track.title }}
								</p>

								<p
									class="text-sm text-muted truncate mt-0.5"
								>
									{{ track.artist }}
								</p>

								<p
									class="text-xs text-muted/70 truncate mt-1"
								>
									{{ track.album }}
								</p>
							</div>

							<!-- Actions -->
							<div
								class="flex items-center gap-3 shrink-0"
							>
								<a
									:href="track.spotify_url"
									target="_blank"
									rel="noopener noreferrer"
									class="hidden sm:block text-xs font-medium text-forest hover:underline"
								>
									Listen
								</a>

								<button
									type="button"
									@click="removeFavorite(track)"
									aria-label="Remove from favorites"
									class="w-9 h-9 rounded-full bg-coral/10 text-coral flex items-center justify-center text-lg hover:bg-coral/20 transition"
								>
									♥
								</button>
							</div>
						</li>
					</ul>
				</div>
			</div>
		</main>
	</div>
</template>
<script setup lang="ts">
import { h } from "vue";
import { toast } from "vue3-toastify";
import { useFavoritesStore } from "@/stores/favorites";
import type { Track } from "@/types/track";
import axios from "axios";

const favorites = useFavoritesStore();

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
						class: "font-semibold underline",
						onClick: async () => {
							try {
								await favorites.addFavorite(track);
								toast.success("Restored!");
							} catch (error) {
	if (axios.isAxiosError(error)) {
		console.error("Failed to restore favorite:", {
			status: error.response?.status,
			data: error.response?.data,
		});
	} else {
		console.error("Failed to restore favorite:", error);
	}

	toast.error("Failed to restore");
}
						},
					},
					"Undo",
				),
			]),
		{
			autoClose: 4000,
		},
	);
}
</script>

<template>
	<main class="min-h-screen overflow-hidden bg-cream">
		<!-- HEADER -->
		<section class="px-5 pb-10 pt-16 sm:px-8 sm:pt-20 lg:px-12">
			<div class="mx-auto max-w-5xl">
				<p
					class="text-[11px] font-bold uppercase tracking-[0.3em] text-accent"
				>
					YOUR COLLECTION
				</p>

				<h1
					class="mt-6 text-5xl font-bold leading-[0.98] tracking-[-0.055em] sm:text-6xl lg:text-7xl"
				>
					Your
					<br class="sm:hidden" />
					<span
						class="bg-linear-to-r from-accent to-purple bg-clip-text text-transparent"
					>
						favorites
					</span>
				</h1>

				<p
					class="mt-6 max-w-xl text-sm leading-6 text-muted sm:text-base sm:leading-7"
				>
					Tracks you've saved for later
				</p>
			</div>
		</section>

		<!-- CONTENT -->
		<section class="mx-auto max-w-5xl px-5 pb-20 sm:px-8 lg:px-12">
			<!-- LOADING -->
			<div
				v-if="!favorites.loaded"
				class="flex items-center justify-center py-20"
			>
				<p class="text-sm text-muted">
					Loading your favorites...
				</p>
			</div>

			<!-- EMPTY STATE -->
			<div
				v-else-if="!favorites.tracks.length"
				class="py-16 text-center sm:py-24"
			>
				<div
					class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-linear-to-br from-accent/15 to-purple/15 text-2xl text-accent"
				>
					♥
				</div>

				<h2 class="mt-5 text-lg font-semibold">
					No favorites yet
				</h2>

				<p
					class="mx-auto mt-2 max-w-sm text-sm leading-6 text-muted"
				>
					Go back to Search and save the tracks you love.
				</p>
			</div>

			<!-- FAVORITES -->
			<div v-else>
				<div class="mb-6">
					<p
						class="text-[11px] font-bold uppercase tracking-[0.25em] text-accent"
					>
						SAVED MUSIC
					</p>

					<h2 class="mt-2 text-2xl font-bold tracking-tight">
						Saved tracks
					</h2>

					<p class="mt-1 text-sm text-muted">
						{{ favorites.tracks.length }}
						{{
							favorites.tracks.length === 1
								? "track"
								: "tracks"
						}}
					</p>
				</div>

				<ul class="grid grid-cols-1 gap-3 md:grid-cols-2">
					<li
						v-for="track in favorites.tracks"
						:key="track.spotify_id"
						class="group flex items-center gap-4 rounded-2xl border border-border bg-white p-3 transition hover:border-accent/30 hover:shadow-sm sm:p-4"
					>
						<!-- COVER -->
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

						<!-- TRACK INFO -->
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

						<!-- ACTIONS -->
						<div class="flex shrink-0 items-center gap-2 sm:gap-3">
							<a
								:href="track.spotify_url"
								target="_blank"
								rel="noopener noreferrer"
								class="hidden rounded-lg px-2 py-2 text-xs font-semibold text-accent transition hover:bg-accent/5 sm:block"
							>
								Listen ↗
							</a>

							<button
								type="button"
								@click="removeFavorite(track)"
								aria-label="Remove from favorites"
								class="flex h-10 w-10 items-center justify-center rounded-full bg-accent/10 text-lg text-accent transition hover:bg-accent/20"
							>
								♥
							</button>
						</div>
					</li>
				</ul>
			</div>
		</section>
	</main>
</template>
<script setup lang="ts">
import { h } from "vue";
import { toast } from "vue3-toastify";
import { useFavoritesStore } from "@/stores/favorites";

const favorites = useFavoritesStore();

async function removeFavorite(track: {
	spotify_id: string;
	title: string;
	artist: string;
	album: string;
	duration_ms: number;
	cover_url: string | null;
	spotify_url: string;
}) {
	try {
		await favorites.removeFavorite(track.spotify_id);
	} catch (e) {
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
							} catch (e) {
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
	<div class="bg-surface border-b border-border">
		<div class="max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
			<h1
				class="font-display font-bold text-3xl sm:text-4xl text-ink mb-2"
			>
				My favorites
			</h1>
			<p class="text-sm sm:text-base text-muted">
				Tracks you've saved for later.
			</p>
		</div>
	</div>

	<main class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
		<p v-if="!favorites.loaded" class="text-sm text-muted">Loading...</p>

		<div
			v-if="favorites.loaded && !favorites.tracks.length"
			class="text-center py-16"
		>
			<p class="text-sm text-muted">
				No favorites yet. Go search for some music.
			</p>
		</div>

		<ul v-if="favorites.tracks.length" class="space-y-1">
			<li
				v-for="track in favorites.tracks"
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
					@click="removeFavorite(track)"
					class="text-lg text-coral shrink-0"
				>
					♥
				</button>
			</li>
		</ul>
	</main>
</template>

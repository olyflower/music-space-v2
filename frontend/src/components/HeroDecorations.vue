<template>
	<!-- Soft background gradients -->
	<div
		class="pointer-events-none absolute -left-48 top-24 -z-10 h-125 w-125 rounded-full bg-accent/10 blur-[100px]"
	></div>

	<div
		class="pointer-events-none absolute -right-48 top-20 -z-10 h-125 w-125 rounded-full bg-purple/10 blur-[100px]"
	></div>

	<div
		class="pointer-events-none absolute -bottom-45 left-1/2 -z-10 h-112.5 w-175 -translate-x-1/2 rounded-full bg-accent/5 blur-[110px]"
	></div>

	<!-- Decorative circles -->
	<div
		class="pointer-events-none absolute -left-70 top-20 -z-10 hidden h-155 w-155 rounded-full border border-accent/40 lg:block"
	></div>

	<div
		class="pointer-events-none absolute -right-70 top-20 -z-10 hidden h-155 w-155 rounded-full border border-purple/40 lg:block"
	></div>
	<!-- Now playing -->
	<div
		class="pointer-events-none absolute left-5 top-37.5 hidden h-44 w-44 rotate-[-10deg] rounded-3xl bg-linear-to-br from-rose-500 via-pink-500 to-purple-500 p-5 shadow-xl lg:block xl:left-12"
	>
		<div class="flex h-full flex-col justify-between text-white">
			<span class="text-[9px] font-bold uppercase tracking-[0.2em]">
				Now playing
			</span>

			<div>
				<div class="text-4xl">♫</div>

				<p class="mt-2 text-sm font-semibold">Feel the sound</p>
			</div>
		</div>
	</div>

	<!-- Good days -->
	<div
		class="pointer-events-none absolute bottom-38.75 left-12 hidden h-36 w-36 rotate-[8deg] rounded-3xl bg-linear-to-br from-sky-300 via-indigo-400 to-purple-500 p-5 shadow-xl lg:block xl:left-20"
	>
		<div class="flex h-full flex-col justify-end text-white">
			<div class="text-3xl">♪</div>

			<p class="mt-1 text-lg font-semibold leading-tight">
				Good<br />
				days
			</p>
		</div>
	</div>

	<!-- Playlist -->
	<div
		class="pointer-events-none absolute right-5 top-37.5 hidden h-44 w-44 rotate-[8deg] rounded-3xl bg-linear-to-br from-slate-700 via-slate-800 to-slate-950 p-5 shadow-xl lg:block xl:right-12"
	>
		<div class="flex h-full flex-col justify-between text-white">
			<span
				class="text-[9px] font-bold uppercase tracking-[0.2em] opacity-60"
			>
				Playlist
			</span>

			<p class="text-xl font-semibold leading-tight">
				Better<br />
				things<br />
				ahead.
			</p>
		</div>
	</div>

	<!-- Vinyl -->
	<div
		class="pointer-events-none absolute bottom-36.25 right-12 hidden h-40 w-40 rotate-[-8deg] items-center justify-center rounded-full bg-ink shadow-xl lg:flex xl:right-20"
	>
		<div
			class="flex h-14 w-14 items-center justify-center rounded-full bg-pink-400 text-xl text-white"
		>
			♫
		</div>
	</div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import { onMounted } from "vue";
import { GoogleLogin } from "vue3-google-login";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

onMounted(() => {
	auth.checkAuth();
});

async function handleGoogleLogin(response: any) {
	await auth.loginWithGoogle(response.credential);
}
</script>

<template>
	<header class="border-b border-gray-100 px-4 py-3">
		<div class="max-w-2xl mx-auto flex items-center justify-between">
			<span class="font-semibold text-gray-900">Music Space</span>

			<div v-if="auth.isLoading" class="text-sm text-gray-400">
				Loading...
			</div>

			<div v-else-if="auth.userEmail" class="flex items-center gap-3">
				<span class="text-sm text-gray-600">{{
					auth.userName || auth.userEmail
				}}</span>
				<button
					@click="auth.logout()"
					class="text-sm text-gray-500 hover:text-gray-900"
				>
					Log out
				</button>
			</div>

			<GoogleLogin v-else :callback="handleGoogleLogin" />
		</div>
	</header>

	<RouterView />
</template>

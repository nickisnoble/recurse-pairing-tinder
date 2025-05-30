<script lang="ts">
	import type { Snippet } from 'svelte';
	import Logo from './Logo.svelte';
	type Props = { children: Snippet };
	const { children }: Props = $props();
</script>

<header class="bg-gray-200 h-24 flex p-4 justify-center fixed bottom-0 left-0 right-0 md:justify-between md:static">
	<div class="hidden md:block">
        <Logo />
    </div>
	<nav class="flex items-center text-center gap-4">
		{@render children()}
	</nav>
</header>
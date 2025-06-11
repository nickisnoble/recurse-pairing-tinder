<script lang="ts">
	import Navigation from '$lib/components/Navigation.svelte';
	import '../app.css';

	let { children } = $props();
</script>

<Navigation/>

{@render children()}
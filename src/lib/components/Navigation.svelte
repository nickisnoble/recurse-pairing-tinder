<script lang="ts">
	import Logo from './Logo.svelte';
	import Button from "$lib/components/Button.svelte";
	import { faBars, faGear, faPlus } from "@fortawesome/free-solid-svg-icons"
</script>

<header class="bg-gray-300 h-24 flex p-4 justify-center fixed bottom-0 left-0 right-0 md:justify-between md:static md:pr-10">
	<div class="hidden md:block">
        <Logo />
    </div>
	<nav class="flex items-center text-center gap-10">
		<Button icon={faBars} onclick={(_) => console.info("you clicked bars")} />
		<Button icon={faPlus} onclick={(_) => console.info("you clicked plus")} large />
		<Button icon={faGear} onclick={(_) => console.info("you clicked gear")} />
	</nav>
</header>
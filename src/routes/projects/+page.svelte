<script lang="ts">
	import Navigation from "$lib/components/Navigation.svelte";
    let links = [{url: "url1", label: "label1"}]
</script>
<Navigation>
  <a class="outline" href="#">hello world</a>
  <a class="outline" href="https://www.google.com">google</a>
</Navigation>
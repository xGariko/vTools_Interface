<script lang="ts">
	import ToolCard from "$lib/components/tool-card.svelte";
	import type  { PageData }  from "./$types"
	import type { ToolCardDTO } from '$lib/models/dto';

	export let data: PageData;
	let toolCards: ToolCardDTO[] = JSON.parse(data.toolCards);
</script>

<div class="fs-2 ms-5 mt-5 w-100 d-flex align-items-center">
	<i class="bi bi-collection text-primary fs-1 me-3"></i>
	<span>Seleziona strumento</span>
</div>

<div class="row overflow-scroll pe-5 ps-5" id="toolCardsList">
	{#each toolCards as toolCard}
		<div class="col-3">
			<ToolCard
				title="{toolCard.title}"
				description="{toolCard.description}"
				route="{toolCard.route}"
				icon="{toolCard.icon}"
			>
			</ToolCard>
		</div>
	{/each}

</div>

<style>
    #toolCardsList{
				height: 80%;
		}
</style>

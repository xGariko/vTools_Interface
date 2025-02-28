<script lang="ts">
	import ToolCard from "$lib/components/tool-card.svelte";
	import type  { PageData }  from "./$types"
	import type { ToolCardDTO } from '$lib/models/dto';

	export let data: PageData;
	let toolCards: ToolCardDTO[] = data.toolCards;

</script>

<div class="fs-2 m-2 row w-100 d-flex align-content-center justify-content-center fw-bold fst-italic">Seleziona tool</div>

<div class="row">
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


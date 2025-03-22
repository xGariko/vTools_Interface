<script>
	import { goto } from '$app/navigation';

	let props = $props();
	let title = props.title;
	let description = props.description;
	let route = props.route;
	let icon = props.icon;

	async function navigate(){
		await goto(route);
	}

	function handleKeyDown(event) {
		// Se l’utente preme Invio (Enter) o Spazio, richiamiamo la stessa funzione di click
		if (event.key === 'Enter' || event.key === ' ') {
			// Impedisce il comportamento di default su Barra Spaziatrice
			event.preventDefault();
			navigate();
		}
	}

</script>

<div
	class="card m-4 mb-0 mt-5"
	onclick={navigate}
	role="link"
	onkeydown={handleKeyDown}
	tabindex="0"
>
	<div class="card-header text-center text-primary fw-bold fs-5">{title}</div>
	{#if icon}
		<div class="card-img d-flex align-items-center justify-content-center text-dark">
			<i class="{icon}"></i>
		</div>
	{/if}
	<div class="card-body pe-5 ps-5 bg-body-tertiary rounded border-top">{description}</div>
</div>

<style>
	.card-img{
			width: 100% !important;
			min-height: 100% !important;
			min-width: 100% !important;
			height: 100px !important;
	}

	.card-img i{
			height: 100% !important;
			font-size: 500%;
	}

	.card{
			transition: 0.2s all;
			cursor: pointer;
	}

	.card:hover{
			transition: 0.2s transform ease-in-out;
			transform: translateY(-2%);
			outline: 2px solid var(--bs-primary);
	}
</style>
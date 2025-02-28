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

</script>

<div class="card m-5">
	<div class="card-header text-center">{title}</div>
	{#if icon}
		<div class="card-img d-flex align-items-center justify-content-center text-dark">
			<i class="{icon}"></i>
		</div>
	{/if}
	<div class="card-body">{description}</div>
	<div class="card-footer">
		<button class="btn btn-primary w-100" onclick={navigate}>Apri</button>
	</div>
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
</style>
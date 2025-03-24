<script>
	let componentProps = $props();
	let title = componentProps.title;
	let icon = componentProps.icon;
</script>

<div class="row">
	<div class="col-12 fs-4 fw-bold text-bg-dark p-3 ps-4">
		<i class="{icon}"></i>
		{title}
	</div>
</div>


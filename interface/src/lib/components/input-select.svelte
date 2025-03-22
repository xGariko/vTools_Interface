<script lang="ts">
	let { value = $bindable(), options = [], name = "", label = null } : { value : string, options : string[], name : string, label : string | null} = $props();


	let label : string = data.label;
	let onChange = data.onchange;

	function callbackChange(){
		onChange()
	}
</script>

{#if label}
	<label for="{name}">{label}</label>
{/if}

<select class="form-select" name="{name}" bind:value={value} onchange={callbackChange}>
	{#each options as option (option)}
		<option value="{option}">{option}</option>
	{/each}
</select>
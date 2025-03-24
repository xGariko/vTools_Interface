<script lang="ts">
	interface InputSelectProps {
		value?: string,
		options?: string[],
		name?: string,
		label?: string | null
		onChange (): void
	}

	let {
		value = $bindable(),
		options = [],
		name = "",
		label = null,
		onChange
	} : InputSelectProps = $props();


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
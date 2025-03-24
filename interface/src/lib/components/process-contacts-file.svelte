<script lang="ts">
	import InputSelect from '$lib/components/input-select.svelte';

	let data = $props();
	let fileData = JSON.parse(JSON.stringify(data)).data;
	console.log(fileData);

	let uploadedFileName = fileData.fileName;
	let columnsNames = fileData.data.headers;

	let surnameColumn = $state("");
	let nameColumn = $state("");
	let unifiedNameColumn = $state("");
	let mobileNumberColumn = $state("");
	let nameFormat = $state("merged");  // Inizialmente settato su "merged"

	let suffix = $state("");
	let prefix = $state("");

	// Gestione del cambio di valore del radio button
	function getNameFormat(event : Event) {
		const target = event.target as HTMLInputElement;
		nameFormat = target.value;
	}

	function formatName(){
		let formattedNames : string[] = [];
		let selectedNames : string[] = [];
		let selectedSurnames : string[] = [];
		let selectedUniqueNames : string[] = [];

		if(nameFormat == "merged"){
			selectedUniqueNames = fileData.data.columnsData[unifiedNameColumn];
			formattedNames = selectedUniqueNames.map((fullName) => {
				return `${prefix} ${fullName ?? ""} ${suffix}`;
			})
			return formattedNames;
		}
		else{
			selectedNames = fileData.data.columnsData[nameColumn];
			selectedSurnames = fileData.data.columnsData[surnameColumn];

			formattedNames = selectedNames.map((name, index) => {
				const surname = selectedSurnames[index];
				return `${prefix} ${name ?? ""} ${surname} ${suffix}`;
			})
			return formattedNames;
		}
	}

	function generateContacts(){
		let formattedNames : string[] = formatName();
		let selectedMobile : string[] = fileData.data.columnsData[mobileNumberColumn];
		// TODO Chiamata API per generare i contatti con python
	}
</script>

<div class="bg-white rounded p-5 m-2">
	<div class="row text-center fs-4">
		<div class="col-12 fw-bold">Dati caricati: <span class="text-primary">{uploadedFileName}</span></div>
	</div>
	<hr style="height:3px;border:none;color:#333;background-color:#333;">
	<div>
		<div id="nameFormat" class="d-flex flex-column p-5">
			<div class="fs-5 mb-3">Seleziona il formato di nome e cognome</div>

			<!-- I radio buttons ora hanno lo stesso 'name' -->
			<div>
				<input type="radio" name="nameType" value="merged" checked onchange={getNameFormat}>
				<label for="nameType">In una colonna</label>
			</div>
			<div>
				<input type="radio" name="nameType" value="separated" onchange={getNameFormat}>
				<label for="nameType">In colonne separate</label>
			</div>
		</div>

		{#if nameFormat === 'separated'}
			<div class="row">
				<div class="col-6">
					<InputSelect
						name="nameColumn"
						options={columnsNames}
						bind:value={nameColumn}
						label="Nome"
						onChange={()=>{}}
					>
					</InputSelect>
				</div>
				<div class="col-6">
					<InputSelect
						name="surnameColumn"
						options={columnsNames}
						label="Cognome"
						bind:value={surnameColumn}
						onChange={()=>{}}
					>
					</InputSelect>
				</div>
			</div>
		{:else}
			<InputSelect
				name="unifiedNameColumn"
				options={columnsNames}
				label="Nome e cognome"
				bind:value={unifiedNameColumn}
				onChange={()=>{}}
			>
			</InputSelect>
		{/if}
	</div>
	<hr>
	<div class="mt-5 row">
		<div class="col-6">
			<InputSelect
				name="mobileNumber"
				options={columnsNames}
				label="Numero di telefono"
				bind:value={mobileNumberColumn}
				onChange={()=>{}}
			>
			</InputSelect>
		</div>

		<div class="col-6 row">
				<div>Aggiungi:</div>
				<div class="col-12 row">
					<div class="col-6">
						<input type="text" class="form-text w-100 text-center" bind:value={prefix} placeholder="Prefisso">
					</div>
					<div class="col-6">
						<input type="text" class="form-text w-100 text-center" bind:value={suffix} placeholder="Suffisso">
					</div>
				</div>
		</div>
	</div>

	<div class="mt-5 pt-5">
		<button class="btn btn-primary w-100" onclick={generateContacts}>Genera</button>
	</div>

</div>
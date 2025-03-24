<script lang="ts">
	import InputSelect from '$lib/components/input-select.svelte';

	let data = $props();

	let callbackFunction = data.callbackFunction;
	let fileData = JSON.parse(JSON.stringify(data)).data;
	console.log(fileData);

	let uploadedFileName = fileData.fileName;
	let columnsNames = fileData.data.headers;

	let surnameColumn: string = $state("");
	let nameColumn: string = $state("");
	let unifiedNameColumn: string = $state("");
	let mobileNumberColumn: string = $state("");
	let nameFormat: string = $state("merged");  // Inizialmente settato su "merged"
	let nFile: number = $state(1);
	let vCardName: string = $state("")

	let suffix = $state("");
	let prefix = $state("");

	let formComplete = $state(false);

	// Gestione del cambio di valore del radio button
	function getNameFormat(event : Event) {
		const target = event.target as HTMLInputElement;

		nameColumn = "";
		surnameColumn = "";
		unifiedNameColumn = "";
		formComplete = false;
		checkCompletion()

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
		callbackFunction({formattedNames, selectedMobile, nFile, vCardName});
	}

	function checkCompletion(){
		if(mobileNumberColumn && mobileNumberColumn !== ""){
			if(
				(unifiedNameColumn && unifiedNameColumn !== "") ||
				( (nameColumn && nameColumn !== "")  && (surnameColumn && nameColumn !== "") )
			){
				formComplete = true;
			}
		}
		else{
			formComplete = false;
		}
	}

	function checkFileDivision(){
		if(nFile < 1){
			nFile = 1
		}
	}
</script>

<div class="bg-white rounded p-5 m-2">
	<div class="row text-center fs-4">
		<div class="col-12 fw-bold">Dati caricati: <span class="text-primary">{uploadedFileName}</span></div>
	</div>
	<hr style="height:3px;border:none;color:#333;background-color:#333;">
	<div>
		<div id="nameFormat" class="d-flex flex-column pt-5">
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
			<div class="row pt-3 pb-3">
				<div class="col-6">
					<InputSelect
						name="nameColumn"
						options={columnsNames}
						bind:value={nameColumn}
						label="Nome *"
						onChange={()=>{}}
					>
					</InputSelect>
				</div>
				<div class="col-6">
					<InputSelect
						name="surnameColumn"
						options={columnsNames}
						label="Cognome *"
						bind:value={surnameColumn}
						onChange={checkCompletion}
					>
					</InputSelect>
				</div>
			</div>
		{:else}
			<div class="pt-3 pb-3">
				<InputSelect
					name="unifiedNameColumn"
					options={columnsNames}
					label="Nome e cognome *"
					bind:value={unifiedNameColumn}
					onChange={checkCompletion}
				>
				</InputSelect>
			</div>
		{/if}
	</div>
	<hr>
	<div class="mt-5 mb-5 row">
		<div class="col-6">
			<InputSelect
				name="mobileNumber"
				options={columnsNames}
				label="Numero di telefono *"
				bind:value={mobileNumberColumn}
				onChange={checkCompletion}
			>
			</InputSelect>
		</div>

		<div class="col-6 row">
				<div>Aggiungi:</div>
				<div class="col-12 row">
					<div class="col-6">
						<input type="text" class="v-input w-100 text-center" bind:value={prefix} placeholder="Prefisso">
					</div>
					<div class="col-6">
						<input type="text" class="v-input w-100 text-center" bind:value={suffix} placeholder="Suffisso">
					</div>
				</div>
		</div>
	</div>
	<hr>
	<div class="row p-2 justify-content-between">
		<div class="col-2">
			<label for="nfile">Dividi in:</label>
			<input type="number"
						 id="nfile"
						 name="nfile"
						 class="v-input"
						 max="100"
						 min="1"
						 bind:value={nFile}
						 onchange={checkFileDivision}
			>
		</div>

		<div class="col-4">
			<label for="nfile">Nome vCard:</label>
			<input type="text" class="v-input w-100 text-center" bind:value={vCardName} placeholder="Nome vCard">
		</div>
	</div>

	<div class="mt-5">
		<button class="btn btn-primary w-100" disabled="{!formComplete}" onclick={generateContacts}>Genera</button>
	</div>

</div>
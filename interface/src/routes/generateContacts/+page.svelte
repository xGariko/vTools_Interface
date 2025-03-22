<script lang="ts">
	import ToolTitle from "$lib/components/tool-title.svelte"
	import UploadFile from "$lib/components/upload-file.svelte"
	import InputSelect from "\$lib/components/input-select.svelte";
	
	import { Config } from '$lib/config';

	let isLoading = $state(false);
	let uploadedFileName = $state(null);
	let isFileUploaded = $state(false);
	let nameFormat = $state("merged");  // Inizialmente settato su "merged"

	let nameColumn = $state("");
	let surnameColumn = $state("");
	let unifiedNameColumn = $state("");

	async function uploadFile(uploadedFile: File) {
		const formData = new FormData();
		formData.append("file", uploadedFile);
		isLoading = true;
		try{
			let response : Response | undefined = await fetch(Config.API_ENDPOINT+"/api/generateContacts/uploadFile", {
				method: 'POST',
				body: formData,
			});
			const data = await response.json();

			if (response.ok) {
				uploadedFileName = data.filename;
				isFileUploaded = true;
			}

		}

		catch(error : unknown) {
			if(error instanceof Error){
				return Promise.reject(error);
			}
			else{
				return null;
			}
		}

		finally {
			isLoading = false;
		}
	}

	// Gestione del cambio di valore del radio button
	function getNameFormat(event : Event) {
		const target = event.target as HTMLInputElement;
		nameFormat = target.value;
		console.log(nameFormat);
	}

	function checklink(){
		console.log(nameColumn);
	}
</script>

<ToolTitle
	title="Genera contatti"
	icon="bi bi-person-rolodex"
></ToolTitle>

<div class="row d-flex justify-content-center">
	<div class="col-9 bg-light p-5">
		{#if !isLoading}
			<UploadFile
				acceptedExtensions={["xlsx", "csv"]}
				onConfirm={uploadFile}
			></UploadFile>
		{:else}
			<div class="w-100 container-fluid d-flex align-items-center justify-content-center p-5">
				<div class="col-10 spinner-grow text-primary" role="status"></div>
				<div class="ms-3 col-auto sr-only text-primary">Caricamento...</div>
			</div>
		{/if}

		{#if !isFileUploaded}
			<div class="bg-white rounded p-5 m-2">
				<div class="row text-center fs-5">
					<div class="col-12">Dati caricati: <span class="text-primary fw-bold">{uploadedFileName}</span></div>
				</div>

				<hr>

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
								options={["ciao","ciao2"]}
								label="Nome"
								onchange={checklink}
							>
							</InputSelect>
						</div>
						<div class="col-6">
							<InputSelect
								name="surnameColumn"
								options={[]}
								label="Cognome"
								bind:value={surnameColumn}
							>
							</InputSelect>
						</div>
					</div>
				{:else}
					<InputSelect
						name="unifiedNameColumn"
						options={[]}
						label="Nome e cognome"
						linkedVar={unifiedNameColumn}
					>
					</InputSelect>
				{/if}
			</div>
		{/if}
	</div>
</div>

<script lang="ts">
	import ToolTitle from "$lib/components/tool-title.svelte"
	import UploadFile from "$lib/components/upload-file.svelte"
	import ProcessContactsFile from "$lib/components/process-contacts-file.svelte";

	import { Config } from '$lib/config';

	let isLoading = $state(false);
	let isFileUploaded = $state(false);
	let fileData = $state(null);


	async function uploadFile(uploadedFile: File) {
		const formData = new FormData();
		formData.append("file", uploadedFile);
		isLoading = true;
		try{
			let response : Response | undefined = await fetch(Config.API_ENDPOINT+"/api/generateContacts/uploadFile", {
				method: 'POST',
				body: formData,
			});
			fileData = await response.json();

			if (response.ok) {
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

		{#if isFileUploaded}
			<ProcessContactsFile
				data={fileData}
			>
			</ProcessContactsFile>

		{/if}
	</div>
</div>

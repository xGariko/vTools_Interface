<!--
	-
	- MiMIT UIBM - GEPI
	-
	- Copyright (C) 2024-25 IBM Consulting Italy - All Rights Reserved
	- This is copyrighted software
	- Unauthorized copying of this file, via any medium is strictly prohibited
	- Proprietary and confidential by IBM Consulting
	-
	-->

<script lang="ts">
	import { formatFileSize } from '$lib/utils/string-utils';
	import { Config } from '$lib/config';

	const props = $props();

	let onConfirm = props.onConfirm;
	let acceptedExtensions: string[] = props.acceptedExtensions || [];
	let acceptedExtensionsString = acceptedExtensions.map(ext => `.${ext}`).join(', ');

	const MAX_FILE_SIZE = Config.MAX_FILE_SIZE;

	let fileInput: HTMLInputElement | undefined = $state();
	let dropZone: HTMLDivElement | undefined = $state();

	let isUploading = $state(false);
	let fileTooLarge = $state(false);
	let invalidExtension = $state(false);

	let selectedFile: File | undefined = $state();

	function handleFileChange() {
		if (!fileInput?.files?.length) return;
		const chosenFile = fileInput.files[0];
		setSelectedFile(chosenFile);
	}

	function handleDrop(event: DragEvent) {
		event.preventDefault();
		const droppedFile = event.dataTransfer?.files[0];
		if (droppedFile) {
			setSelectedFile(droppedFile);
		}
	}

	function handleDragOver(event: DragEvent) {
		event.preventDefault();
	}

	function setSelectedFile(file: File) {
		selectedFile = file;
		fileTooLarge = selectedFile.size > MAX_FILE_SIZE;
		const ext = selectedFile.name.split('.').pop()?.toLowerCase() || '';
		invalidExtension = !acceptedExtensions.includes(ext);
	}



	function deleteSelectedFile() {
		selectedFile = undefined;
		fileTooLarge = false;
		invalidExtension = false;
	}



	function confirmUpload() {
		if(selectedFile && !isUploading && !fileTooLarge) {
			onConfirm(selectedFile);
			deleteSelectedFile()
		}
	}


</script>

<div class="row m-lg-2 mb-lg-3 p-lg-4 p-1 bg-white border rounded">
	<div class="col-12">
		{#if fileTooLarge}
			<div class="alert alert-danger" role="alert">
				<img src="/svg/file-upload-error.svg"  class="d-none d-lg-block" width="200" height="200" alt="upload-error">
				Il file selezionato è troppo grande. La dimensione massima consentita è di 25 MB.
			</div>
			<button class="btn btn-warning w-100" onclick="{deleteSelectedFile}">Riprova</button>
		{:else if invalidExtension}
			<div class="alert alert-danger" role="alert">
				<img src="/svg/file-upload-error.svg" class="d-none d-lg-block" width="200" height="200" alt="upload-error">
				Il tipo di file selezionato non è supportato. Le estensioni consentite sono: <span class="fw-bold">{acceptedExtensionsString}</span>.
			</div>
			<button class="btn btn-warning w-100" onclick="{deleteSelectedFile}">Riprova</button>
		{:else if !selectedFile && !isUploading}
			<div
				class="mt-0 mt-lg-2 border-dashed border border-primary rounded p-2 p-lg-5 d-flex flex-row align-items-center justify-content-start"
				bind:this="{dropZone}"
				ondragover="{handleDragOver}"
				ondrop="{handleDrop}"
				role="presentation">

				<div class="me-lg-5">
					<img src="/svg/file-upload.svg" alt="" class="d-none d-lg-block" width="150" height="150" id="upload-file-image">
				</div>
				<div>
					<div class="h4 text-primary">Trascina il file per caricarlo</div>
					<div class="h6 text-secondary">
						Oppure
						<label for="fileInput" class="link-primary text-decoration-underline" style="cursor: pointer">
							selezionalo dal dispositivo
						</label>
					</div>
					<div class="text-secondary">(Max. 25 MB)</div>
				</div>


			</div>
		{:else if selectedFile && !fileTooLarge}
			<div class="mt-2 border-dashed border border-primary rounded p-5 d-flex flex-column align-items-start justify-content-start">
				<div class="h4 text">
					Hai selezionato il file: <span class="h4 text-primary">{selectedFile.name}</span>
				</div>
				<div class="h5 text-secondary">
					Dimensione file: <span>{formatFileSize(selectedFile.size)}</span>
				</div>
				<button class="btn btn-outline-dark mt-2" onclick="{deleteSelectedFile}">
					<i class="bi bi-x"></i>
					Elimina file selezionato
				</button>
			</div>
			<button class="btn btn-primary col-12 mt-3" onclick="{confirmUpload}">
				Carica informazioni
			</button>

		{/if}

		<input
			type="file"
			id="fileInput"
			class="d-none"
			bind:this="{fileInput}"
			accept="{acceptedExtensionsString}"
			onchange="{handleFileChange}" />
	</div>

</div>

<style>
    .border-dashed {
        border-style: dashed !important;
    }


</style>

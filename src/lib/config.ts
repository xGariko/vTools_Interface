import type { ConfigType } from '$lib/models/dto';

const API_ENDPOINT : string = "https://vtools-a9g7.onrender.com";
const MAX_FILE_SIZE = 25 * 1024 * 1024;

export const Config : ConfigType = {
	API_ENDPOINT : API_ENDPOINT,
	MAX_FILE_SIZE : MAX_FILE_SIZE
}
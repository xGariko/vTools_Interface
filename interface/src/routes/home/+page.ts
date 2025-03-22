import type { PageLoad } from './$types';
import { Config } from '$lib/config';
import { ApiCall } from '$lib/api-call';

export const load: PageLoad = async({ fetch }) =>{
	const toolConfigResponseEndpoint : string = `${Config.API_ENDPOINT}/api/config/tool_cards`;

	const apiCall = new ApiCall
	const toolConfigResponse = await apiCall.get(fetch, toolConfigResponseEndpoint);
	if (!toolConfigResponse || (toolConfigResponse.status !== 404 && toolConfigResponse.status !== 200)){
		throw new Error("Unable to load tool cards from API");
	}
	if(toolConfigResponse.status === 404){
		return {
			toolCards: null
		}
	}

	if(toolConfigResponse.status === 200){
		const toolCards = await toolConfigResponse.json();
		return {
			toolCards: toolCards
		}
	}

}
type Fetch = (info: RequestInfo | URL, init?: RequestInit) => Promise<Response>;

export class ApiCall {
	async post(fetch: Fetch, endpoint: string, body: object): Promise<Response | null> {
		return this.wrappedFetch(fetch, endpoint, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});
	}

	async get(fetch: Fetch, endpoint: string): Promise<Response | null> {
		return this.wrappedFetch(fetch, endpoint, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Accept': 'application/json'
			}
		});
	}

	async delete(fetch: Fetch, endpoint: string): Promise<void> {
		await this.wrappedFetch(fetch, endpoint, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

	async patch(fetch: Fetch, endpoint: string, body: string): Promise<Response | null> {
		return this.wrappedFetch(fetch, endpoint, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body
		});
	}

	async put(fetch: Fetch, endpoint: string, body: string): Promise<Response | null> {
		return this.wrappedFetch(fetch, endpoint, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body
		});
	}

	private async wrappedFetch(
		fetch: Fetch,
		endpoint: string,
		options: RequestInit
	): Promise<Response | null> {
		return await fetch(endpoint, options);
	}
}

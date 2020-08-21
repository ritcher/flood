import httpx

api = httpx.Client(
	base_url='https://lojaonline.vivo.com.br',
	max_redirects=0,
	timeout=None,
	verify=False
)

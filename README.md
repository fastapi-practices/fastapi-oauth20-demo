# FastAPI OAuth 2.0 Demo

A demo application for [fastapi-oauth20](https://github.com/fastapi-practices/fastapi-oauth20) library, demonstrating
OAuth 2.0 integration with multiple providers.

## Quick Start

1. Install dependencies:

```bash
uv sync
```

2. Create `.env` file:

```bash
cp .env.example .env
```

3. Configure OAuth credentials in `.env`:

4. Configure callback URLs in your OAuth applications:

   ```
   http://localhost:8000/api/v1/oauth2/{provider}/callback
   ```

   Where `{provider}` is: `github`, `google`, `feishu`, `gitee`, `linux-do`, `oschina`

5. Run the application:

   ```bash
   python main.py
   ```

6. Open http://localhost:8000

## License

[MIT](https://github.com/fastapi-practices/fastapi-oauth20-demo/blob/master/LICENSE)

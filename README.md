# Goutam Nifty Live — Ready Repo

This repository is ready to upload to GitHub. The GitHub Actions workflow will build a Windows single-file executable (`.exe`) using PyInstaller.

## Steps

1. Create a new GitHub repository (private or public).
2. Upload all files from this zip to the repo root.
3. Commit and push to `main`.
4. On GitHub, go to **Actions** → run the `Build Windows EXE` workflow, or just push to `main`.
5. When the run completes, download the artifact `goutam-nifty-live-exe` from the workflow run.
6. Run the `.exe` on your Windows machine. It will open a Streamlit UI and ask for your Access Token.

## Notes

- The bundled `smartapi_client.py` may need minor adjustments to match Angel One's WebSocket messages or endpoint.
- The app prompts for your Access Token at runtime — do not share your credentials.
- If you need me to update `smartapi_client.py` to use instrument tokens or a specific WS endpoint, provide the error messages and I will patch it.
import json
import asyncio
from pathlib import Path
from .config import LEADS_PORT, LEADS_MAX_BODY

async def serve_leads(project_dir: str, port: int = LEADS_PORT) -> None:
    lf = Path(project_dir) / "leads.json"

    async def handler(reader, writer):
        rl = (await reader.readline()).decode("utf-8", errors="replace")
        parts = rl.split(" ", 2)
        if len(parts) < 2:
            writer.close()
            return
        method, path = parts[0], parts[1]
        if method == "POST" and path == "/save-lead":
            body = b""
            while True:
                chunk = await reader.read(1024)
                if not chunk:
                    break
                body += chunk
                if len(body) > LEADS_MAX_BODY:
                    break
            try:
                lead = json.loads(body.decode("utf-8"))
                leads = []
                if lf.exists():
                    leads = json.loads(lf.read_text(encoding="utf-8"))
                leads.append(lead)
                lf.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
                resp, st = '{"status":"ok"}', "200 OK"
            except (json.JSONDecodeError, OSError):
                resp, st = '{"status":"error"}', "400 Bad Request"
        elif method == "GET" and path == "/leads":
            resp = lf.read_text(encoding="utf-8") if lf.exists() else "[]"
            st = "200 OK"
        else:
            resp, st = '{"status":"not_found"}', "404 Not Found"
        writer.write(f"HTTP/1.1 {st}\r\n".encode())
        writer.write(b"Content-Type: application/json\r\n")
        writer.write(b"Access-Control-Allow-Origin: *\r\n")
        writer.write(f"Content-Length: {len(resp)}\r\n".encode())
        writer.write(b"\r\n")
        writer.write(resp.encode())
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(handler, "127.0.0.1", port)
    async with server:
        await server.serve_forever()

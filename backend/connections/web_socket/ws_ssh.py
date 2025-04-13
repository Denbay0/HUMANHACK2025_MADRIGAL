import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connections.session_manager import session_manager

router = APIRouter()

@router.websocket("/ws/ssh/{session_id}")
async def websocket_ssh(websocket: WebSocket, session_id: str):
    await websocket.accept()
    if session_id not in session_manager.sessions:
        await websocket.send_text("Сессия не найдена")
        await websocket.close()
        return

    connection = session_manager.sessions[session_id]
    try:
        shell = connection.open_shell()
        shell.send("\r")
        await websocket.send_text("Подключение установлено...\n")
    except Exception as e:
        await websocket.send_text(f"Ошибка открытия интерактивного режима: {e}")
        await websocket.close()
        return

    loop = asyncio.get_event_loop()

    async def read_from_ssh():
        while True:
            try:
                if shell.exit_status_ready():
                    break
                if shell.recv_ready():
                    data = shell.recv(1024)
                    if data:
                        await websocket.send_text(data.decode(errors='replace'))
                await asyncio.sleep(0.1)
            except Exception as e:
                await websocket.send_text(f"\nОшибка при чтении: {e}\n")
                break

    read_task = asyncio.create_task(read_from_ssh())

    try:
        while True:
            client_data = await websocket.receive_text()
            try:
                await loop.run_in_executor(None, shell.send, client_data)
            except Exception as e:
                await websocket.send_text(f"\nОшибка при отправке данных: {e}\n")
    except WebSocketDisconnect:
        read_task.cancel()
        try:
            connection.close()
        except Exception:
            pass

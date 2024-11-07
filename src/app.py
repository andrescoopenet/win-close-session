import os
import win32ts
from dotenv import load_dotenv


def get_sessions(usuarios: list) -> list:
    server = None
    sesiones_info = win32ts.WTSEnumerateSessions(server, 1, 0)
    sessions = []
    for session in sesiones_info:
        session_id = session['SessionId']
        nombre_usuario = win32ts.WTSQuerySessionInformation(
            server, session_id, win32ts.WTSUserName
        )
        if nombre_usuario in usuarios:
            sessions.append(session_id)
    return sessions


# Lista las sesiones activas y cierra la sesión de una específica
def cerrar_sesion_usuario(session_id):
    try:
        win32ts.WTSLogoffSession(None, session_id, True)
        print(f"Sesión {session_id} cerrada exitosamente.")
    except Exception as e:
        print(f"Error cerrando sesión {session_id}: {e}")


def main():
    session_id = get_sessions(os.getenv('USUARIOS').split(','))
    for session in session_id:
        cerrar_sesion_usuario(session)
    print("Finalizado.")


if __name__ == '__main__':
    load_dotenv()
    main()

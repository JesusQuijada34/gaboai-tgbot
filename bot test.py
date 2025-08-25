
import os
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

CONFIG_FILE = "config/credentials.json"

def load_or_create_credentials():
    # Carga el archivo de credenciales o lo crea si no existe
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        creds = {}
    else:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)

    # Pedir token si no existe
    if "token" not in creds:
        creds["token"] = input("Introduce el token del bot de Telegram: ").strip()

    # Pedir channel_id y group_id si no existen
    if "channel_id" not in creds:
        creds["channel_id"] = input("Introduce el channel_id (puedes dejar vacío si no aplica): ").strip()
    if "group_id" not in creds:
        creds["group_id"] = input("Introduce el group_id (puedes dejar vacío si no aplica): ").strip()

    # Elegir entre channel_id y group_id
    if creds.get("channel_id") and creds.get("group_id"):
        print("¿Dónde quieres que el bot publique mensajes?")
        print("1. Canal (channel_id)")
        print("2. Grupo (group_id)")
        opcion = input("Elige 1 o 2: ").strip()
        if opcion == "1":
            creds["target_id"] = creds["channel_id"]
        elif opcion == "2":
            creds["target_id"] = creds["group_id"]
        else:
            print("Opción inválida, se usará channel_id por defecto.")
            creds["target_id"] = creds["channel_id"]
    elif creds.get("channel_id"):
        creds["target_id"] = creds["channel_id"]
    elif creds.get("group_id"):
        creds["target_id"] = creds["group_id"]
    else:
        print("Debes proporcionar al menos un channel_id o group_id.")
        exit(1)

    # Guardar credenciales actualizadas
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(creds, f, indent=2, ensure_ascii=False)

    return creds

async def show_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    print(f"Chat title: {chat.title}")
    print(f"Chat ID: {chat.id}")
    await context.bot.send_message(
        chat_id=chat.id, 
        text=f"Este chat ID es: `{chat.id}`", 
        parse_mode="Markdown"
    )

def main():
    creds = load_or_create_credentials()
    app = Application.builder().token(creds["token"]).build()
    app.add_handler(MessageHandler(filters.ALL, show_chat_id))
    print("Bot corriendo. Escribe un mensaje en tu grupo o canal para ver el chat ID.")
    app.run_polling()

if __name__ == "__main__":
    main()

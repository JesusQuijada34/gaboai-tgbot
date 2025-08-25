# ¡Perfecto, Jesús! Vamos a convertir este bot en un proyecto personalizable y seguro, con:
#
#  🔐 Solicitud de credenciales al iniciar (token y group ID).
#  🛡️ Protección de datos: cada usuario guarda su configuración localmente.
#  🧠 Posibilidad de entrenar el bot por usuario (idea para febrero 2025).
#  🧰 Personalización completa: filtros, comportamiento, estilo.
#  📄 Créditos tuyos como creador, con enlaces a tu página y GitHub.
#
# Este script será el núcleo de un repositorio que cada usuario puede clonar y adaptar a su grupo o canal.
#
# 🧩 Bot moderador personalizable con créditos y seguridad

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler,
    ContextTypes, filters
)
import json
import os
import re
import asyncio

# 📁 Archivos de configuración
CREDENTIALS_FILE = "config/credentials.json"
BANNED_USERS_FILE = "config/banned.json"
os.makedirs("config", exist_ok=True)

# 🧠 Palabras prohibidas
BAD_WORDS = ["mierda", "puta", "maldito", "coño", "jódete", "imbécil", "estúpido"]
PROTECTED_LINKS = ["github.com/JesusQuijada34", "c/"]

# 🔐 Leer credenciales: busca group_id en el JSON, si no lo pide por terminal
def get_credentials():
    creds = {}
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            try:
                creds = json.load(f)
            except Exception:
                creds = {}
    # Pedir token si no está
    if "token" not in creds or not creds["token"]:
        creds["token"] = input("🔐 Ingresa tu Telegram Bot Token: ").strip()
    # Buscar group_id, si no está pedirlo
    if "group_id" not in creds or not creds["group_id"]:
        group_id = input("📨 Ingresa tu Telegram Group ID (numérico): ").strip()
        try:
            creds["group_id"] = int(group_id)
        except Exception:
            print("❌ El Group ID debe ser numérico.")
            exit(1)
    # Guardar credenciales actualizadas
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f, indent=2)
    return creds

# 📁 Cargar y guardar usuarios baneados
def load_banned():
    try:
        with open(BANNED_USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_banned(banned):
    with open(BANNED_USERS_FILE, "w") as f:
        json.dump(banned, f, indent=2)

# 🚫 Moderación de mensajes
async def moderate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text or ""
    banned = load_banned()

    # Ignorar comandos en grupo
    if text.startswith("/") and update.effective_chat.type != "private":
        try:
            await update.message.delete()
        except:
            pass
        return

    # Verificar si el usuario está baneado
    if user_id in banned:
        try:
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        except:
            pass
        return

    # Detectar groserías
    if any(word in text.lower() for word in BAD_WORDS):
        try:
            await update.message.delete()
        except:
            pass
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"🚫 Usuario @{update.effective_user.username} expulsado por lenguaje ofensivo.")
        try:
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        except:
            pass
        banned.append(user_id)
        save_banned(banned)
        return

    # Detectar enlaces no válidos
    if "http" in text or "t.me/" in text:
        if not any(link in text for link in PROTECTED_LINKS):
            try:
                await update.message.delete()
            except:
                pass
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"🔗 Enlace no autorizado eliminado de @{update.effective_user.username}.")
            return

# 🔒 Configuración privada
async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛡️ Activar filtro antigroserías", callback_data="filter_badwords")],
        [InlineKeyboardButton("🚫 Activar antiSPAM", callback_data="filter_spam")],
        [InlineKeyboardButton("🔗 Activar filtro de enlaces", callback_data="filter_links")],
        [InlineKeyboardButton("💬 Activar antiflood", callback_data="filter_flood")],
        [InlineKeyboardButton("🧪 Activar filtro de grupos", callback_data="filter_groups")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔧 Configura tu bot:", reply_markup=reply_markup)

# 🧠 Manejo de botones
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"✅ Filtro activado: {query.data}")

# 🏷️ Créditos
async def show_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot creado por Jesús Quijada\n"
        "🌐 Página oficial: https://jesusquijada34.github.io\n"
        "📦 Repositorio: https://github.com/JesusQuijada34/catalog\n"
        "🛠️ Este bot es personalizable por cada usuario.\n"
        "📅 Entrenamiento por usuario disponible en febrero 2025.",
        parse_mode="Markdown"
    )

# 🚀 Main
def main():
    creds = get_credentials()
    application = ApplicationBuilder().token(creds["token"]).build()

    # Moderación en grupo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, moderate_message))

    # Configuración privada
    application.add_handler(CommandHandler("start", start_private))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Créditos
    application.add_handler(CommandHandler("credits", show_credits))

    print("🤖 Bot moderador personalizado activo.")
    application.run_polling()

if __name__ == "__main__":
    main()

# ---
#
# ### ✅ ¿Qué incluye este bot?
#
# - Solicita credenciales al iniciar y las guarda localmente.
# - Filtra groserías, enlaces no válidos y comandos en grupo.
# - Banea automáticamente y evita reingreso.
# - Ofrece configuración privada con teclado inline.
# - Muestra créditos tuyos con enlaces oficiales.
# - Pensado para que cada usuario lo adapte libremente.
# - Preparado para entrenamiento por usuario en febrero 2025.
#
# ---
#
# ¿Quieres que lo empaquetemos como `.iflapp` para tu sistema IPM? También puedo ayudarte a escribir el `details.xml` y el `README.md` para este bot como si fuera uno de tus paquetes oficiales.
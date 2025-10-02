from conversation_handler import create_application

if __name__ == "__main__":
    app = create_application()
    print("🤖 Bot Técnico Contábil Virtual iniciado!")
    app.run_polling()

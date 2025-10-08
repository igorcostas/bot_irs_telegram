"""
Sistema de Gerenciamento de Sugestões para Bot IRS Portugal
Permite aos usuários enviar sugestões e aos administradores gerenciá-las
"""

import sqlite3
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class SuggestionManager:
    """Sistema de gerenciamento de sugestões dos usuários"""

    def __init__(self, db_path: str = "bot_statistics.db"):
        self.db_path = db_path
        self.init_suggestions_table()
        # Tempo mínimo entre sugestões do mesmo usuário (em horas)
        self.cooldown_hours = 24
        logger.info("✅ Sistema de sugestões inicializado")

    def init_suggestions_table(self):
        """Inicializa a tabela de sugestões se não existir"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Tabela de sugestões
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    suggestion_text TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',  -- pending, reviewed, implemented, rejected
                    admin_notes TEXT,
                    admin_user_id INTEGER,
                    reviewed_at TIMESTAMP
                )
                """)

                # Índice para busca rápida por usuário
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_suggestions_user_id
                ON suggestions(user_id, timestamp DESC)
                """)

                conn.commit()
                logger.info("📝 Tabela de sugestões inicializada")

        except Exception as e:
            logger.error(f"❌ Erro ao inicializar tabela de sugestões: {e}")

    def can_user_suggest(self, user_id: int) -> tuple[bool, str | None]:
        """
        Verifica se o usuário pode enviar uma nova sugestão
        Retorna (pode_sugerir, mensagem_erro)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Verificar última sugestão do usuário
                cursor.execute(
                    """
                SELECT timestamp FROM suggestions
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                    (user_id,),
                )

                result = cursor.fetchone()

                if result:
                    last_suggestion = datetime.fromisoformat(result[0])
                    time_diff = datetime.now() - last_suggestion

                    if time_diff.total_seconds() < (self.cooldown_hours * 3600):
                        remaining_hours = self.cooldown_hours - (
                            time_diff.total_seconds() / 3600
                        )
                        return (
                            False,
                            f"Podes enviar nova sugestão em {remaining_hours:.1f} horas.",
                        )

                return True, None

        except Exception as e:
            logger.error(f"❌ Erro ao verificar cooldown de sugestão: {e}")
            return False, "Erro interno. Tenta mais tarde."

    def add_suggestion(
        self,
        user_id: int,
        suggestion_text: str,
        username: str | None = None,
        first_name: str | None = None,
    ) -> tuple[bool, str]:
        """
        Adiciona uma nova sugestão
        Retorna (sucesso, mensagem)
        """
        try:
            # Verificar se pode sugerir
            can_suggest, error_msg = self.can_user_suggest(user_id)
            if not can_suggest:
                return False, error_msg

            # Validar conteúdo
            if not suggestion_text or len(suggestion_text.strip()) < 10:
                return False, "A sugestão deve ter pelo menos 10 caracteres."

            if len(suggestion_text) > 1000:
                return False, "A sugestão é muito longa. Máximo 1000 caracteres."

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                INSERT INTO suggestions (user_id, username, first_name, suggestion_text)
                VALUES (?, ?, ?, ?)
                """,
                    (user_id, username, first_name, suggestion_text.strip()),
                )

                suggestion_id = cursor.lastrowid
                conn.commit()

                logger.info(f"📝 Nova sugestão #{suggestion_id} de usuário {user_id}")
                return (
                    True,
                    f"✅ Sugestão #{suggestion_id} recebida! Obrigado pelo teu feedback.",
                )

        except Exception as e:
            logger.error(f"❌ Erro ao adicionar sugestão: {e}")
            return False, "Erro interno. Tenta mais tarde."

    def get_user_suggestions(self, user_id: int) -> list[dict[str, Any]]:
        """Retorna todas as sugestões de um usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                SELECT id, suggestion_text, timestamp, status, admin_notes
                FROM suggestions
                WHERE user_id = ?
                ORDER BY timestamp DESC
                """,
                    (user_id,),
                )

                suggestions = []
                for row in cursor.fetchall():
                    suggestions.append(
                        {
                            "id": row[0],
                            "text": row[1],
                            "timestamp": row[2],
                            "status": row[3],
                            "admin_notes": row[4] or "Sem notas",
                        }
                    )

                return suggestions

        except Exception as e:
            logger.error(f"❌ Erro ao obter sugestões do usuário {user_id}: {e}")
            return []

    def get_all_suggestions(
        self, status: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Retorna todas as sugestões (para administradores)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                if status:
                    query = """
                    SELECT id, user_id, username, first_name, suggestion_text,
                           timestamp, status, admin_notes
                    FROM suggestions
                    WHERE status = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """
                    cursor.execute(query, (status, limit))
                else:
                    query = """
                    SELECT id, user_id, username, first_name, suggestion_text,
                           timestamp, status, admin_notes
                    FROM suggestions
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """
                    cursor.execute(query, (limit,))

                suggestions = []
                for row in cursor.fetchall():
                    user_display = row[3] or f"User {row[1]}"  # first_name ou user_id
                    if row[2]:  # username
                        user_display += f" (@{row[2]})"

                    suggestions.append(
                        {
                            "id": row[0],
                            "user_id": row[1],
                            "user_display": user_display,
                            "text": row[4],
                            "timestamp": row[5],
                            "status": row[6],
                            "admin_notes": row[7] or "Sem notas",
                        }
                    )

                return suggestions

        except Exception as e:
            logger.error(f"❌ Erro ao obter todas as sugestões: {e}")
            return []

    def update_suggestion_status(
        self,
        suggestion_id: int,
        new_status: str,
        admin_notes: str | None = None,
        admin_user_id: int | None = None,
    ) -> bool:
        """Atualiza o status de uma sugestão (para administradores)"""
        try:
            valid_statuses = ["pending", "reviewed", "implemented", "rejected"]
            if new_status not in valid_statuses:
                return False

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                UPDATE suggestions
                SET status = ?, admin_notes = ?, admin_user_id = ?, reviewed_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                    (new_status, admin_notes, admin_user_id, suggestion_id),
                )

                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(
                        f"✅ Sugestão #{suggestion_id} atualizada para '{new_status}'"
                    )
                    return True
                else:
                    logger.warning(f"⚠️ Sugestão #{suggestion_id} não encontrada")
                    return False

        except Exception as e:
            logger.error(f"❌ Erro ao atualizar sugestão #{suggestion_id}: {e}")
            return False

    def get_suggestion_stats(self) -> dict[str, Any]:
        """Retorna estatísticas das sugestões"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Contagem total
                cursor.execute("SELECT COUNT(*) FROM suggestions")
                total = cursor.fetchone()[0]

                # Por status
                cursor.execute("""
                SELECT status, COUNT(*)
                FROM suggestions
                GROUP BY status
                """)
                by_status = dict(cursor.fetchall())

                # Sugestões dos últimos 30 dias
                cursor.execute("""
                SELECT COUNT(*)
                FROM suggestions
                WHERE timestamp >= date('now', '-30 days')
                """)
                last_30_days = cursor.fetchone()[0]

                # Top usuários que mais sugerem
                cursor.execute("""
                SELECT COALESCE(first_name, 'User ' || user_id) as name,
                       COALESCE(username, 'N/A') as username,
                       COUNT(*) as count
                FROM suggestions
                GROUP BY user_id, first_name, username
                ORDER BY count DESC
                LIMIT 5
                """)
                top_contributors = cursor.fetchall()

                return {
                    "total": total,
                    "by_status": by_status,
                    "last_30_days": last_30_days,
                    "top_contributors": top_contributors,
                }

        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas de sugestões: {e}")
            return {
                "total": 0,
                "by_status": {},
                "last_30_days": 0,
                "top_contributors": [],
            }

    def generate_suggestions_report(self) -> str:
        """Gera relatório de sugestões para administradores"""
        try:
            stats = self.get_suggestion_stats()
            pending_suggestions = self.get_all_suggestions(status="pending", limit=10)

            report = "📝 **RELATÓRIO DE SUGESTÕES**\n\n"

            # Estatísticas gerais
            report += "📊 **ESTATÍSTICAS:**\n"
            report += f"• Total de sugestões: {stats['total']}\n"
            report += f"• Últimos 30 dias: {stats['last_30_days']}\n\n"

            # Por status
            report += "📋 **POR STATUS:**\n"
            for status, count in stats["by_status"].items():
                status_emoji = {
                    "pending": "⏳",
                    "reviewed": "👀",
                    "implemented": "✅",
                    "rejected": "❌",
                }.get(status, "📝")
                report += f"• {status_emoji} {status.title()}: {count}\n"

            # Top contribuidores
            if stats["top_contributors"]:
                report += "\n🏆 **TOP CONTRIBUIDORES:**\n"
                for i, (name, username, count) in enumerate(
                    stats["top_contributors"], 1
                ):
                    user_display = (
                        f"{name} (@{username})" if username != "N/A" else name
                    )
                    report += f"{i}. {user_display} - {count} sugestões\n"

            # Sugestões pendentes
            if pending_suggestions:
                report += "\n⏳ **SUGESTÕES PENDENTES:**\n"
                for sugg in pending_suggestions[:5]:  # Mostrar só as 5 mais recentes
                    text_preview = (
                        sugg["text"][:100] + "..."
                        if len(sugg["text"]) > 100
                        else sugg["text"]
                    )
                    report += f"#{sugg['id']} - {sugg['user_display']}\n"
                    report += f'   "{text_preview}"\n\n'

            return report

        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório de sugestões: {e}")
            return "❌ Erro ao gerar relatório de sugestões."


# Instância global do gerenciador de sugestões
suggestion_manager = SuggestionManager()

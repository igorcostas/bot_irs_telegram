"""
Sistema de Monitoramento para Bot IRS Portugal
Tracking de usuários, comandos e estatísticas gerais
"""

import sqlite3
import logging
from datetime import datetime
from typing import Any


logger = logging.getLogger(__name__)


class BotMonitoring:
    """Sistema de monitoramento e estatísticas do bot"""

    def __init__(self, db_path: str = "bot_statistics.db"):
        self.db_path = db_path
        self.init_database()
        logger.info("✅ Sistema de monitoramento inicializado")

    def init_database(self):
        """Inicializa o banco de dados e cria tabelas se necessário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Tabela de usuários
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_interactions INTEGER DEFAULT 1
                )
                """)

                # Tabela de comandos/mensagens
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    activity_type TEXT,  -- 'command', 'message', 'question'
                    content TEXT,        -- comando usado ou pergunta feita
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
                """)

                # Tabela de estatísticas gerais
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    key TEXT PRIMARY KEY,
                    value INTEGER DEFAULT 0
                )
                """)

                # Inicializar contadores básicos se não existirem
                cursor.execute("""
                INSERT OR IGNORE INTO statistics (key, value) VALUES
                ('total_users', 0),
                ('total_messages', 0),
                ('total_commands', 0),
                ('total_simulations', 0),
                ('total_suggestions', 0),
                ('completed_simulations', 0)
                """)

                conn.commit()
                logger.info("📊 Database inicializada com sucesso")

        except Exception as e:
            logger.error(f"❌ Erro ao inicializar database: {e}")

    def register_user(
        self,
        user_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        """Registra ou atualiza informações de um usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Verificar se usuário já existe
                cursor.execute(
                    "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
                )
                exists = cursor.fetchone()

                if exists:
                    # Atualizar última visita e incrementar interações
                    cursor.execute(
                        """
                    UPDATE users
                    SET last_seen = CURRENT_TIMESTAMP,
                        total_interactions = total_interactions + 1,
                        username = COALESCE(?, username),
                        first_name = COALESCE(?, first_name),
                        last_name = COALESCE(?, last_name)
                    WHERE user_id = ?
                    """,
                        (username, first_name, last_name, user_id),
                    )
                else:
                    # Inserir novo usuário
                    cursor.execute(
                        """
                    INSERT INTO users (user_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                    """,
                        (user_id, username, first_name, last_name),
                    )

                    # Incrementar contador total de usuários
                    cursor.execute("""
                    UPDATE statistics SET value = value + 1 WHERE key = 'total_users'
                    """)

                conn.commit()
                logger.debug(f"👤 Usuário {user_id} registrado/atualizado")

        except Exception as e:
            logger.error(f"❌ Erro ao registrar usuário {user_id}: {e}")

    def register_activity(self, user_id: int, activity_type: str, content: str):
        """Registra uma atividade do usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Inserir atividade
                cursor.execute(
                    """
                INSERT INTO user_activities (user_id, activity_type, content)
                VALUES (?, ?, ?)
                """,
                    (user_id, activity_type, content),
                )

                # Incrementar contadores relevantes
                if activity_type == "command":
                    cursor.execute(
                        "UPDATE statistics SET value = value + 1 WHERE key = 'total_commands'"
                    )
                    if content == "/simular":
                        cursor.execute(
                            "UPDATE statistics SET value = value + 1 WHERE key = 'total_simulations'"
                        )
                    elif content == "/sugestoes":
                        cursor.execute(
                            "UPDATE statistics SET value = value + 1 WHERE key = 'total_suggestions'"
                        )
                elif activity_type == "message":
                    cursor.execute(
                        "UPDATE statistics SET value = value + 1 WHERE key = 'total_messages'"
                    )

                conn.commit()
                logger.debug(f"📝 Atividade registrada: {activity_type} - {content}")

        except Exception as e:
            logger.error(f"❌ Erro ao registrar atividade: {e}")

    def register_simulation_completion(self, user_id: int):
        """Registra que um usuário completou uma simulação de IRS"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE statistics SET value = value + 1 WHERE key = 'completed_simulations'
                """)
                conn.commit()
                logger.debug(
                    f"✅ Simulação completada registrada para usuário {user_id}"
                )
        except Exception as e:
            logger.error(f"❌ Erro ao registrar simulação completada: {e}")

    def get_engagement_metrics(self) -> dict[str, float]:
        """Retorna métricas de engagement para showcase"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Taxa de retorno (usuários com mais de 1 interação)
                cursor.execute("""
                SELECT
                    COUNT(CASE WHEN total_interactions > 1 THEN 1 END) * 100.0 / COUNT(*) as return_rate
                FROM users
                """)
                return_rate = cursor.fetchone()[0] or 0

                # Média de interações por usuário
                cursor.execute("SELECT AVG(total_interactions) FROM users")
                avg_interactions = cursor.fetchone()[0] or 0

                # Taxa de simulações completadas
                cursor.execute(
                    "SELECT value FROM statistics WHERE key = 'total_simulations'"
                )
                simulations = cursor.fetchone()[0] if cursor.fetchone() else 0
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM users")
                total_users = cursor.fetchone()[0] or 1
                simulation_rate = (
                    (simulations * 100.0) / total_users if total_users > 0 else 0
                )

                return {
                    "return_rate": round(return_rate, 2),
                    "avg_interactions_per_user": round(avg_interactions, 2),
                    "simulation_completion_rate": round(simulation_rate, 2),
                }

        except Exception as e:
            logger.error(f"❌ Erro ao obter métricas de engagement: {e}")
            return {
                "return_rate": 0,
                "avg_interactions_per_user": 0,
                "simulation_completion_rate": 0,
            }

    def get_usage_patterns(self) -> dict[str, any]:
        """Retorna padrões de uso para análise de cliente"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Horários de pico (hora do dia com mais atividades)
                cursor.execute("""
                SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
                FROM user_activities
                GROUP BY hour
                ORDER BY count DESC
                LIMIT 3
                """)
                peak_hours = cursor.fetchall()

                # Dias da semana mais ativos
                cursor.execute("""
                SELECT
                    CASE cast(strftime('%w', timestamp) as integer)
                        WHEN 0 THEN 'Domingo'
                        WHEN 1 THEN 'Segunda'
                        WHEN 2 THEN 'Terça'
                        WHEN 3 THEN 'Quarta'
                        WHEN 4 THEN 'Quinta'
                        WHEN 5 THEN 'Sexta'
                        WHEN 6 THEN 'Sábado'
                    END as day_name,
                    COUNT(*) as count
                FROM user_activities
                GROUP BY strftime('%w', timestamp)
                ORDER BY count DESC
                LIMIT 3
                """)
                active_days = cursor.fetchall()

                # Crescimento de usuários (últimos 7 dias)
                cursor.execute("""
                SELECT DATE(first_seen) as date, COUNT(*) as new_users
                FROM users
                WHERE first_seen >= date('now', '-7 days')
                GROUP BY DATE(first_seen)
                ORDER BY date DESC
                """)
                growth_pattern = cursor.fetchall()

                return {
                    "peak_hours": [
                        f"{hour}:00h ({count} atividades)" for hour, count in peak_hours
                    ],
                    "most_active_days": [
                        f"{day} ({count} atividades)" for day, count in active_days
                    ],
                    "growth_last_7_days": len(growth_pattern),
                    "daily_growth": growth_pattern,
                }

        except Exception as e:
            logger.error(f"❌ Erro ao obter padrões de uso: {e}")
            return {"peak_hours": [], "most_active_days": [], "growth_last_7_days": 0}

    def get_general_stats(self) -> dict[str, int]:
        """Retorna estatísticas gerais do bot"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT key, value FROM statistics")
                stats = dict(cursor.fetchall())

                # Adicionar dados calculados
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM users")
                stats["unique_users"] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM user_activities")
                stats["total_activities"] = cursor.fetchone()[0]

                return stats

        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas gerais: {e}")
            return {}

    def get_top_users(self, limit: int = 10) -> list[tuple[Any, ...]]:
        """Retorna top usuários por número de interações"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT user_id, COALESCE(username, 'N/A') as username,
                       COALESCE(first_name, 'N/A') as first_name,
                       total_interactions, last_seen
                FROM users
                ORDER BY total_interactions DESC
                LIMIT ?
                """,
                    (limit,),
                )
                return cursor.fetchall()

        except Exception as e:
            logger.error(f"❌ Erro ao obter top usuários: {e}")
            return []

    def get_top_commands(self, limit: int = 10) -> list[tuple[Any, ...]]:
        """Retorna top comandos mais usados"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT content, COUNT(*) as usage_count
                FROM user_activities
                WHERE activity_type = 'command'
                GROUP BY content
                ORDER BY usage_count DESC
                LIMIT ?
                """,
                    (limit,),
                )
                return cursor.fetchall()

        except Exception as e:
            logger.error(f"❌ Erro ao obter top comandos: {e}")
            return []

    def get_top_questions(self, limit: int = 10) -> list[tuple[Any, ...]]:
        """Retorna top perguntas/mensagens mais comuns"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT content, COUNT(*) as usage_count
                FROM user_activities
                WHERE activity_type IN ('message', 'question')
                AND LENGTH(content) < 100  -- Evitar textos muito longos
                GROUP BY LOWER(content)    -- Case insensitive
                ORDER BY usage_count DESC
                LIMIT ?
                """,
                    (limit,),
                )
                return cursor.fetchall()

        except Exception as e:
            logger.error(f"❌ Erro ao obter top perguntas: {e}")
            return []

    def get_user_stats(self, user_id: int) -> dict[str, Any] | None:
        """Retorna estatísticas de um usuário específico"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Dados básicos do usuário
                cursor.execute(
                    """
                SELECT username, first_name, total_interactions, first_seen, last_seen
                FROM users WHERE user_id = ?
                """,
                    (user_id,),
                )

                user_data = cursor.fetchone()
                if not user_data:
                    return None

                # Contar atividades por tipo
                cursor.execute(
                    """
                SELECT activity_type, COUNT(*)
                FROM user_activities
                WHERE user_id = ?
                GROUP BY activity_type
                """,
                    (user_id,),
                )

                activities = dict(cursor.fetchall())

                return {
                    "username": user_data[0] or "N/A",
                    "first_name": user_data[1] or "N/A",
                    "total_interactions": user_data[2],
                    "first_seen": user_data[3],
                    "last_seen": user_data[4],
                    "activities": activities,
                }

        except Exception as e:
            logger.error(f"❌ Erro ao obter stats do usuário {user_id}: {e}")
            return None

    def get_daily_stats(self, days: int = 7) -> list[tuple[Any, ...]]:
        """Retorna estatísticas dos últimos N dias"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT DATE(timestamp) as date,
                       COUNT(*) as activities,
                       COUNT(DISTINCT user_id) as unique_users
                FROM user_activities
                WHERE timestamp >= date('now', '-{} days')
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
                """.format(days)
                )
                return cursor.fetchall()

        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas diárias: {e}")
            return []

    def generate_showcase_report(self) -> str:
        """Gera relatório específico para showcase a clientes"""
        try:
            # Estatísticas básicas
            general_stats = self.get_general_stats()
            engagement_metrics = self.get_engagement_metrics()
            usage_patterns = self.get_usage_patterns()

            # Top usuários e comandos
            top_users = self.get_top_users(5)
            top_commands = self.get_top_commands(5)

            # Montar relatório de showcase
            report = "🚀 **RELATÓRIO DE PERFORMANCE - BOT IRS PORTUGAL**\n"
            report += "_Demonstração de Capacidades para Novos Clientes_\n\n"

            # KPIs principais
            report += "📊 **INDICADORES-CHAVE DE PERFORMANCE (KPIs):**\n"
            report += f"• **Usuários Ativos**: {general_stats.get('unique_users', 0)}\n"
            report += f"• **Total de Interações**: {general_stats.get('total_activities', 0):,}\n"
            report += f"• **Simulações de IRS Realizadas**: {general_stats.get('total_simulations', 0)}\n"
            report += (
                f"• **Taxa de Retorno**: {engagement_metrics.get('return_rate', 0)}%\n"
            )
            report += f"• **Média de Interações/Usuário**: {engagement_metrics.get('avg_interactions_per_user', 0)}\n"
            report += f"• **Taxa de Conversão (Simulações)**: {engagement_metrics.get('simulation_completion_rate', 0)}%\n\n"

            # Padrões de uso
            if usage_patterns.get("peak_hours"):
                report += "⏰ **HORÁRIOS DE MAIOR ENGAJAMENTO:**\n"
                for hour in usage_patterns["peak_hours"]:
                    report += f"• {hour}\n"
                report += "\n"

            if usage_patterns.get("most_active_days"):
                report += "📅 **DIAS MAIS ATIVOS DA SEMANA:**\n"
                for day in usage_patterns["most_active_days"]:
                    report += f"• {day}\n"
                report += "\n"

            # Funcionalidades mais usadas
            report += "🔥 **FUNCIONALIDADES MAIS POPULARES:**\n"
            for i, (command, count) in enumerate(top_commands, 1):
                report += f"{i}. **{command}** - {count} utilizações\n"
            report += "\n"

            # Crescimento
            report += f"📈 **CRESCIMENTO RECENTE:**\n"
            report += f"• Novos usuários (7 dias): {usage_patterns.get('growth_last_7_days', 0)}\n\n"

            # Informações técnicas finais
            report += "🔧 **SISTEMA TÉCNICO:**\n"
            report += "• ✅ Monitoramento em tempo real\n"
            report += "• ✅ Base de dados SQLite integrada\n"
            report += "• ✅ API Groq para processamento de linguagem\n"
            report += "• ✅ Sistema de feedback dos usuários\n"
            report += "• ✅ Relatórios automatizados\n\n"

            report += "ℹ️ **Para mais informações, use o comando** `/contato`"

            return report

        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório de showcase: {e}")
            return "❌ Erro ao gerar relatório de showcase."

    def generate_stats_report(self) -> str:
        """Gera relatório completo de estatísticas"""
        try:
            # Estatísticas gerais
            general_stats = self.get_general_stats()

            # Top usuários
            top_users = self.get_top_users(10)

            # Top comandos
            top_commands = self.get_top_commands(10)

            # Top perguntas
            top_questions = self.get_top_questions(10)

            # Estatísticas diárias
            daily_stats = self.get_daily_stats(7)

            # Montar relatório
            report = "📊 **RELATÓRIO DE ESTATÍSTICAS DO BOT IRS**\n\n"

            # Estatísticas gerais
            report += "🔢 **ESTATÍSTICAS GERAIS:**\n"
            report += (
                f"• Total de usuários únicos: {general_stats.get('unique_users', 0)}\n"
            )
            report += (
                f"• Total de atividades: {general_stats.get('total_activities', 0)}\n"
            )
            report += f"• Total de comandos: {general_stats.get('total_commands', 0)}\n"
            report += (
                f"• Total de simulações: {general_stats.get('total_simulations', 0)}\n"
            )
            report += (
                f"• Total de sugestões: {general_stats.get('total_suggestions', 0)}\n\n"
            )

            # Top usuários
            report += "👥 **TOP 10 USUÁRIOS:**\n"
            for i, (
                user_id,
                username,
                first_name,
                interactions,
                last_seen,
            ) in enumerate(top_users, 1):
                name = (
                    f"{first_name} (@{username})" if username != "N/A" else first_name
                )
                report += f"{i}. {name} - {interactions} interações (última: {last_seen[:10]})\n"

            # Top comandos
            report += "\n🤖 **TOP 10 COMANDOS:**\n"
            for i, (command, count) in enumerate(top_commands, 1):
                report += f"{i}. {command} - {count} usos\n"

            # Top perguntas
            report += "\n❓ **TOP 10 PERGUNTAS/MENSAGENS:**\n"
            for i, (question, count) in enumerate(top_questions, 1):
                # Truncar pergunta se muito longa
                question_short = (
                    question[:50] + "..." if len(question) > 50 else question
                )
                report += f'{i}. "{question_short}" - {count} vezes\n'

            # Atividade dos últimos 7 dias
            report += "\n📅 **ATIVIDADE DOS ÚLTIMOS 7 DIAS:**\n"
            for date, activities, unique_users in daily_stats:
                report += f"• {date}: {activities} atividades, {unique_users} usuários únicos\n"

            return report

        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            return "❌ Erro ao gerar relatório de estatísticas."


# Instância global do sistema de monitoramento
monitoring = BotMonitoring()

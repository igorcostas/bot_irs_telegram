# conversation_handler.py
from main_integration import PostAnalysisHandler
import re
from telegram import Update
from telegram.ext import ContextTypes

from irs_calculator import IRSCalculator, get_tax_bracket

QUESTIONS = [
    "1) Qual é o seu estado civil? (solteiro, casado, união de facto)",
    "2) Qual é o seu tipo de trabalho? (dependente/assalariado, independente/autônomo)",
    "3) Para qual ano fiscal? (ex.: 2024)",
    "4) Quantos dependentes? (0 se nenhum)",
    "5) Qual é a sua idade? (em anos)",
    "6) Reside fiscalmente em Portugal todo o ano? (sim/não)",
    "7) Qual o rendimento anual bruto do trabalho (€)?",
    "8) Tem outras rendas? (sim/não)",
    "9) Se sim, total de outras rendas (€)?",
    "10) Retenções na fonte do trabalho (€) no ano?",
    "11) Contribuições para a Segurança Social (€)?",
    "12) Despesas de saúde dedutíveis (€)?",
    "13) Despesas de educação dedutíveis (€)?",
    "14) Encargos com habitação dedutíveis (€)?",
    "15) Despesas com lares ou familiares dedutíveis (€)?",
    "16) Tem benefícios específicos? (IRS Jovem, deficiente, etc.) sim/não",
    "17) Se sim, quais? (texto curto)",
    "18) Pagou pensões de alimentos dedutíveis? sim/não",
    "19) Se sim, total anual (€)?",
    "20) Deseja tributação conjunta? (apenas se casado/união) sim/não",
]

KEYS = [
    "civil_status", "job_type", "tax_year", "dependents", "age", "pt_resident",
    "gross_salary", "has_other_income", "other_income", "withholdings",
    "social_security", "health_exp", "education_exp", "housing_exp",
    "care_exp", "has_benefits", "benefits_detail", "alimony_paid",
    "alimony_total", "joint_taxation",
]

irs_calculator = IRSCalculator()

def clean_number(text: str) -> str:
    s = text.lower().strip().replace("€", "").replace(" euros", "").replace(" euro", "")
    m = re.match(r"^\s*(\d+(?:[\.,]\d+)?)\s*mil\s*$", s)
    if m:
        v = float(m.group(1).replace(",", "."))
        return str(v * 1_000)
    if s == "mil":
        return "1000"
    s = s.replace(".", "").replace(",", ".")
    nums = re.findall(r"(\d+(?:\.\d+)?)", s)
    return nums[0] if nums else ""

def match_job_type(text: str) -> str | None:
    t = text.lower()
    if any(x in t for x in ("dependente", "assalariado")):
        return "dependente"
    if any(x in t for x in ("independente", "autônomo", "autonomo")):
        return "independente"
    return None

def is_yes_no(text: str) -> bool:
    return text.lower() in ("sim", "não", "nao")

async def handle_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step", 0)
    text = update.message.text.strip()

    # 1) Estado civil
    if step == 0:
        context.user_data["civil_status"] = text
        context.user_data["step"] = 1
        return await update.message.reply_text(QUESTIONS[1])

    # 2) Tipo de trabalho
    if step == 1:
        jt = match_job_type(text)
        if not jt:
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[1])
        context.user_data["job_type"] = jt
        context.user_data["step"] = 2
        return await update.message.reply_text(QUESTIONS[2])

    # 3) Ano fiscal
    if step == 2:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[2])
        context.user_data["tax_year"] = float(num)
        context.user_data["step"] = 3
        return await update.message.reply_text(QUESTIONS[3])

    # 4) Dependentes
    if step == 3:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[3])
        context.user_data["dependents"] = float(num)
        context.user_data["step"] = 4
        return await update.message.reply_text(QUESTIONS[4])

    # 5) Idade
    if step == 4:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[4])
        context.user_data["age"] = float(num)
        context.user_data["step"] = 5
        return await update.message.reply_text(QUESTIONS[5])

    # 6) Reside em PT?
    if step == 5:
        if not is_yes_no(text):
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[5])
        context.user_data["pt_resident"] = text.lower()
        context.user_data["step"] = 6
        return await update.message.reply_text(QUESTIONS[6])

    # 7) Rendimento bruto
    if step == 6:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[6])
        context.user_data["gross_salary"] = float(num)
        context.user_data["step"] = 7
        return await update.message.reply_text(QUESTIONS[7])

    # 8) Outras rendas?
    if step == 7:
        if not is_yes_no(text):
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[7])
        ctx = text.lower()
        context.user_data["has_other_income"] = ctx
        if ctx in ("nao", "não"):
            context.user_data["other_income"] = 0.0
            context.user_data["step"] = 9
            return await update.message.reply_text(QUESTIONS[9])
        else:
            context.user_data["step"] = 8
            return await update.message.reply_text(QUESTIONS[8])

    # 9) Valor de outras rendas
    if step == 8:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[8])
        context.user_data["other_income"] = float(num)
        context.user_data["step"] = 9
        return await update.message.reply_text(QUESTIONS[9])

    # 10) Retenções
    if step == 9:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[9])
        context.user_data["withholdings"] = float(num)
        context.user_data["step"] = 10
        return await update.message.reply_text(QUESTIONS[10])

    # 11) Segurança Social
    if step == 10:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[10])
        context.user_data["social_security"] = float(num)
        context.user_data["step"] = 11
        return await update.message.reply_text(QUESTIONS[11])

    # 12) Saúde
    if step == 11:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[11])
        context.user_data["health_exp"] = float(num)
        context.user_data["step"] = 12
        return await update.message.reply_text(QUESTIONS[12])

    # 13) Educação
    if step == 12:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[12])
        context.user_data["education_exp"] = float(num)
        context.user_data["step"] = 13
        return await update.message.reply_text(QUESTIONS[13])

    # 14) Habitação
    if step == 13:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[13])
        context.user_data["housing_exp"] = float(num)
        context.user_data["step"] = 14
        return await update.message.reply_text(QUESTIONS[14])

    # 15) Lares/familiares
    if step == 14:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[14])
        context.user_data["care_exp"] = float(num)
        context.user_data["step"] = 15
        return await update.message.reply_text(QUESTIONS[15])

    # 16) Benefícios
    if step == 15:
        if not is_yes_no(text):
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[15])
        ctx = text.lower()
        context.user_data["has_benefits"] = ctx
        if ctx == "sim":
            context.user_data["step"] = 16
            return await update.message.reply_text(QUESTIONS[16])
        else:
            context.user_data["benefits_detail"] = ""
            context.user_data["step"] = 17
            return await update.message.reply_text(QUESTIONS[17])

    # 17) Quais benefícios
    if step == 16:
        context.user_data["benefits_detail"] = text
        context.user_data["step"] = 17
        return await update.message.reply_text(QUESTIONS[17])

    # 18) Pensão alimentícia?
    if step == 17:
        if not is_yes_no(text):
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[17])
        ctx = text.lower()
        context.user_data["alimony_paid"] = ctx
        if ctx == "sim":
            context.user_data["step"] = 18
            return await update.message.reply_text(QUESTIONS[18])
        else:
            context.user_data["alimony_total"] = 0.0
            context.user_data["step"] = 19
            return await update.message.reply_text(QUESTIONS[19])

    # 19) Total pensão
    if step == 18:
        num = clean_number(text)
        if not num:
            return await update.message.reply_text("❌ Digite valor. " + QUESTIONS[18])
        context.user_data["alimony_total"] = float(num)
        context.user_data["step"] = 19
        return await update.message.reply_text(QUESTIONS[19])

    # 20) Tributação conjunta
    if step == 19:
        if not is_yes_no(text):
            return await update.message.reply_text("❌ Inválido. " + QUESTIONS[19])
        context.user_data["joint_taxation"] = text.lower()
        data = {k: context.user_data[k] for k in KEYS}
        return await finalize_simulation(update, context, data)


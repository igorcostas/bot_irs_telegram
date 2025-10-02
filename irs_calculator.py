import config

class IRSCalculator:
    def __init__(self):
        self.brackets = config.TAX_BRACKETS
        self.deductions = config.DEDUCTIONS

    def calculate_full(self,data:dict)->dict:
        income=data["gross_salary"]+(data["other_income"] if data["has_other_income"]=="sim" else 0)
        deductible=self.deductions.get("specific_a",0)
        taxable=max(0,income-deductible)
        total_ded=(data["health_exp"]*self.deductions["health"]["rate"]+
                   data["education_exp"]*self.deductions["education"]["rate"]+
                   data["housing_exp"]*self.deductions["housing"]["rate"])
        taxable=max(0,taxable-total_ded)
        gross=0; breakdown=[]; rem=taxable
        for nm,br in self.brackets.items():
            if rem<=0: break
            lo=br["min"]; hi=br["max"] or float("inf")
            if taxable>lo:
                amt=min(rem,hi-lo); tx=amt*br["rate"]
                gross+=tx; breakdown.append((nm.replace("escalao_",""),amt,br["rate"],tx))
                rem-=amt
        net=gross-data["withholdings"]-data["social_security"]
        verdict=f"pagará {net:.2f}€" if net>0 else f"receberá {abs(net):.2f}€"
        summary=(f"**Rendimento bruto:**{income:.2f}€\n"
                 f"**Tributável:**{taxable:.2f}€\n"
                 f"**Imposto bruto:**{gross:.2f}€\n"
                 f"**Retenções+SS:**{data['withholdings']+data['social_security']:.2f}€\n"
                 f"**Imposto líquido:**{net:.2f}€\n"
                 f"**Veredito:**{verdict}")
        details=["Dedução específica:"+f"{deductible:.2f}€","Deduções:"]
        for e,a,r,t in breakdown:
            details.append(f"-{e}:{a:.2f}€ @{r*100:.1f}%={t:.2f}€")
        return{"verdict":verdict,"summary":summary,"details":"\n".join(details)}

    def format_result(self,res:dict)->str:
        return res["summary"]+"\n\nEnvie 'detalhes' para ver cálculo completo."

def get_tax_bracket(income:float)->dict:
    for name,br in config.TAX_BRACKETS.items():
        lo=br["min"]; hi=br["max"] or float("inf")
        if lo<=income<=hi:
            return{"escalão":name.replace("escalao_",""),"mínimo":lo,
                   "máximo":None if br["max"] is None else hi,"taxa":br["rate"]}
    nm,br=list(config.TAX_BRACKETS.items())[-1]
    return{"escalão":nm.replace("escalao_",""),"mínimo":br["min"],"máximo":None,"taxa":br["rate"]}

